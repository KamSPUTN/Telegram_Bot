#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import io
import time
import shutil
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import datetime, time as dt_time
import asyncio
import logging
import pytz
import nest_asyncio
import pandas as pd
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

# Применяем nest_asyncio для обхода проблем с event loop
nest_asyncio.apply()

# Настройка московского времени
os.environ['TZ'] = 'Europe/Moscow'

# Настройка логирования для отладки
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('bot_final_working.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Конфигурация
TOKEN = '7576144966:AAHM9B-Yih0FRcaC3fQEKkFa3S7W1aFdexE'
GROUP_CHAT_ID = -4982684830  # Первая группа
GROUP_CHAT_ID_2 = -542407478  # Вторая группа для напоминаний
EXCEL_FILE = 'reminders.xlsx'
BACKUP_FILE = 'reminders_backup.xlsx'
MAX_RETRIES = 3  # Максимальное количество попыток чтения файла
RETRY_DELAY = 2  # Задержка между попытками в секундах
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1rojWrTFYKv0j06iSH7Aex9faEvDjbjYG/edit?gid=1984600935#gid=1984600935"

logger = logging.getLogger(__name__)


class FinalWorkingReminderBot:
    def __init__(self):
        """Инициализация бота"""
        self.application = ApplicationBuilder().token(TOKEN).build()
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.reminders = []
        self.last_successful_read = None
        self.setup_handlers()

    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("test", self.test_command))
        self.application.add_handler(CommandHandler("time", self.time_command))
        self.application.add_handler(CommandHandler("send", self.send_message_command))
        self.application.add_handler(CommandHandler("check", self.check_excel_command))
        self.application.add_handler(CommandHandler("debug", self.debug_command))
        self.application.add_handler(CommandHandler("group", self.check_group_command))
        self.application.add_handler(CommandHandler("load", self.load_reminders_command))
        self.application.add_handler(CommandHandler("list", self.list_reminders_command))
        self.application.add_handler(CommandHandler("reload", self.reload_reminders_command))

    def safe_read_excel(self, retries=MAX_RETRIES):
        """Безопасное чтение Excel файла с повторными попытками"""
        for attempt in range(retries):
            try:
                if not os.path.exists(EXCEL_FILE):
                    logger.error(f"❌ Файл {EXCEL_FILE} не найден!")
                    return None

                try:
                    shutil.copy2(EXCEL_FILE, BACKUP_FILE)
                    logger.info(f"✅ Создана резервная копия {BACKUP_FILE}")
                except Exception as e:
                    logger.warning(f"⚠️ Не удалось создать резервную копию: {e}")

                try:
                    df = pd.read_excel(EXCEL_FILE)
                    self.last_successful_read = datetime.now()
                    logger.info(f"✅ Файл {EXCEL_FILE} успешно прочитан")
                    return df
                except Exception as main_e:
                    logger.warning(f"⚠️ Ошибка чтения основного файла: {main_e}")

                    if os.path.exists(BACKUP_FILE):
                        try:
                            df = pd.read_excel(BACKUP_FILE)
                            logger.info(f"✅ Прочитана резервная копия {BACKUP_FILE}")
                            return df
                        except Exception as backup_e:
                            logger.error(f"❌ Ошибка чтения резервной копии: {backup_e}")

                if attempt < retries - 1:
                    logger.info(f"⏳ Ожидание {RETRY_DELAY} секунд перед следующей попыткой...")
                    time.sleep(RETRY_DELAY)

            except Exception as e:
                logger.error(f"❌ Ошибка при попытке чтения файла (попытка {attempt + 1}): {e}")
                if attempt < retries - 1:
                    time.sleep(RETRY_DELAY)

        logger.error(f"❌ Не удалось прочитать файл после {retries} попыток")
        return None

    def read_reminders_from_excel(self):
        """Чтение напоминаний из Excel файла"""
        try:
            logger.info(f"Проверяю файл: {EXCEL_FILE}")
            
            df = self.safe_read_excel()
            if df is None:
                return []
            
            logger.info(f"Прочитано {len(df)} строк")
            logger.info(f"Колонки: {df.columns.tolist()}")
            
            reminders = []
            
            for index, row in df.iterrows():
                try:
                    logger.info(f"Обрабатываю строку {index + 1}")
                    
                    date_str = row.get('Дата', None)
                    if pd.isna(date_str):
                        logger.warning(f"Пропускаю строку {index + 1}: нет даты")
                        continue
                    
                    try:
                        reminder_date = pd.to_datetime(date_str).date()
                        logger.info(f"Дата напоминания: {reminder_date}")
                    except Exception as e:
                        logger.error(f"❌ Ошибка парсинга даты {date_str}: {e}")
                        continue
                    
                    current_date = datetime.now(pytz.timezone('Europe/Moscow')).date()
                    if reminder_date < current_date:
                        logger.warning(f"Пропускаю строку {index + 1}: дата {reminder_date} уже прошла")
                        continue
                    
                    time_str = row.get('Время', row.get('Time', row.get('время', '')))
                    message = row.get('Сообщение', row.get('Message', row.get('сообщение', '')))
                    
                    if pd.isna(time_str) or pd.isna(message):
                        logger.warning(f"Пропускаю строку {index + 1}: пустые данные")
                        continue
                    
                    try:
                        # Исправленная обработка времени
                        if isinstance(time_str, str):
                            if ':' in time_str:
                                hour, minute = map(int, time_str.split(':')[:2])
                                parsed_time = dt_time(hour, minute)
                            else:
                                parsed_time = pd.to_datetime(time_str).time()
                        elif hasattr(time_str, 'time'):
                            parsed_time = time_str.time()
                        elif isinstance(time_str, dt_time):
                            parsed_time = time_str
                        elif hasattr(time_str, 'hour') and hasattr(time_str, 'minute'):
                            # Это уже объект datetime.time
                            parsed_time = time_str
                        else:
                            parsed_time = pd.to_datetime(time_str).time()
                            
                        logger.info(f"Время напоминания: {parsed_time}")
                    except Exception as e:
                        logger.error(f"❌ Ошибка парсинга времени {time_str}: {e}")
                        continue
                    
                    reminder = {
                        'date': reminder_date,
                        'time': parsed_time,
                        'message': str(message),
                        'row': index + 1
                    }
                    
                    reminders.append(reminder)
                    logger.info(f"✅ Добавлено напоминание: {reminder_date} {parsed_time.strftime('%H:%M')} - {message[:30]}")
                    
                except Exception as e:
                    logger.error(f"❌ Ошибка обработки строки {index + 1}: {e}")
                    continue
            
            logger.info(f"Всего загружено напоминаний: {len(reminders)}")
            return reminders
            
        except Exception as e:
            logger.error(f"❌ Ошибка чтения Excel файла: {e}")
            return []

    def schedule_reminders(self):
        """Планирование напоминаний"""
        try:
            logger.info("Планирую напоминания...")
            self.scheduler.remove_all_jobs()
            logger.info("Очищены старые задачи")
            
            moscow_tz = pytz.timezone('Europe/Moscow')
            
            for reminder in self.reminders:
                try:
                    reminder_datetime = datetime.combine(
                        reminder['date'],
                        reminder['time']
                    )
                    reminder_datetime = moscow_tz.localize(reminder_datetime)
                    
                    now = datetime.now(moscow_tz)
                    if reminder_datetime <= now:
                        logger.warning(f"Пропускаю напоминание {reminder['row']}: время {reminder_datetime} уже прошло")
                        continue
                    
                    job_id = f"reminder_{reminder['row']}"
                    
                    self.scheduler.add_job(
                        func=self.send_reminder,
                        trigger=DateTrigger(
                            run_date=reminder_datetime,
                            timezone=moscow_tz
                        ),
                        args=[reminder['message']],
                        id=job_id,
                        replace_existing=True
                    )
                    
                    logger.info(f"✅ Запланировано: {reminder_datetime} - {reminder['message'][:30]}")
                    
                except Exception as e:
                    logger.error(f"❌ Ошибка планирования напоминания: {e}")
                    continue
                    
            logger.info(f"Всего запланировано задач: {len(self.scheduler.get_jobs())}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка планирования: {e}")

    async def send_reminder(self, message):
        """Отправка напоминания в обе группы"""
        try:
            moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
            full_message = (
                f"⏰ НАПОМИНАНИЕ!\n\n"
                f"{message}\n\n"
                f"🕐 {moscow_time.strftime('%H:%M:%S')}\n\n"
                f"[График]({SPREADSHEET_URL}) Жми для просмотра"
            )
            
            logger.info(f"Отправляю напоминание: {message[:30]}")
            
            try:
                await self.application.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=full_message,
                    parse_mode='Markdown'
                )
                logger.info("✅ Напоминание отправлено в группу 1!")
            except Exception as e:
                logger.error(f"❌ Ошибка отправки в группу 1: {e}")
            
            try:
                await self.application.bot.send_message(
                    chat_id=GROUP_CHAT_ID_2,
                    text=full_message,
                    parse_mode='Markdown'
                )
                logger.info("✅ Напоминание отправлено в группу 2!")
            except Exception as e:
                logger.error(f"❌ Ошибка отправки в группу 2: {e}")
            
        except Exception as e:
            logger.error(f"❌ Ошибка отправки напоминания: {e}")

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /start"""
        await update.message.reply_text(
            "🤖 ОБНОВЛЕННЫЙ бот запущен! ✅\n\n"
            "Команды:\n"
            "/check - проверить Excel файл\n"
            "/load - загрузить напоминания\n"
            "/list - список напоминаний\n"
            "/reload - перезагрузить\n"
            "/status - статус бота\n"
            "/debug - отладочная информация\n"
            "/test - тест бота\n"
            "/group - проверить группу"
        )
        logger.info(f"Пользователь {update.effective_user.id} запустил ОБНОВЛЕННОГО бота")

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /status"""
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
        status_msg = [
            "🤖 Статус ОБНОВЛЕННОГО бота:",
            f"🕐 Московское время: {moscow_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"📋 Загружено напоминаний: {len(self.reminders)}",
            f"📁 Excel файл: {'✅' if os.path.exists(EXCEL_FILE) else '❌'}",
            f"📁 Резервная копия: {'✅' if os.path.exists(BACKUP_FILE) else '❌'}"
        ]
        
        if self.last_successful_read:
            status_msg.append(f"📅 Последнее успешное чтение: {self.last_successful_read.strftime('%Y-%m-%d %H:%M:%S')}")
        
        status_msg.extend([
            f"👥 Группа 1 ID: {GROUP_CHAT_ID}",
            f"👥 Группа 2 ID: {GROUP_CHAT_ID_2}",
            f"⏰ Запланировано задач: {len(self.scheduler.get_jobs())}"
        ])
        
        jobs = self.scheduler.get_jobs()
        if jobs:
            status_msg.append("\n📅 Ближайшие напоминания:")
            for job in sorted(jobs, key=lambda x: x.next_run_time)[:3]:
                status_msg.append(f"- {job.next_run_time.strftime('%Y-%m-%d %H:%M')}")
        
        status_msg.append("✅ Бот работает!")
        await update.message.reply_text("\n".join(status_msg))
        logger.info(f"Пользователь {update.effective_user.id} запросил статус")

    async def check_group_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /group"""
        try:
            await update.message.reply_text("👥 Проверяю доступ к группам...")
            
            try:
                chat1 = await self.application.bot.get_chat(GROUP_CHAT_ID)
                await update.message.reply_text(
                    f"✅ Группа 1 найдена: {chat1.title}\n"
                    f"👥 Участников: {chat1.member_count if hasattr(chat1, 'member_count') else 'неизвестно'}"
                )
                logger.info(f"✅ Группа 1 доступна: {chat1.title}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка доступа к группе 1: {e}")
                logger.error(f"❌ Ошибка доступа к группе 1: {e}")
            
            try:
                chat2 = await self.application.bot.get_chat(GROUP_CHAT_ID_2)
                await update.message.reply_text(
                    f"✅ Группа 2 найдена: {chat2.title}\n"
                    f"👥 Участников: {chat2.member_count if hasattr(chat2, 'member_count') else 'неизвестно'}"
                )
                logger.info(f"✅ Группа 2 доступна: {chat2.title}")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка доступа к группе 2: {e}")
                logger.error(f"❌ Ошибка доступа к группе 2: {e}")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка проверки групп: {e}")
            logger.error(f"❌ Ошибка проверки групп: {e}")

    async def debug_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /debug"""
        try:
            moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
            debug_msg = [
                "🔍 ОТЛАДОЧНАЯ ИНФОРМАЦИЯ:\n",
                f"🕐 Время: {moscow_time.strftime('%Y-%m-%d %H:%M:%S')}",
                f"📋 Напоминаний: {len(self.reminders)}",
                f"⏰ Задач в планировщике: {len(self.scheduler.get_jobs())}",
                f"📁 Файл Excel: {'✅' if os.path.exists(EXCEL_FILE) else '❌'}",
                f"📁 Резервная копия: {'✅' if os.path.exists(BACKUP_FILE) else '❌'}"
            ]
            
            if self.last_successful_read:
                debug_msg.append(f"📅 Последнее успешное чтение: {self.last_successful_read.strftime('%Y-%m-%d %H:%M:%S')}")
            
            debug_msg.extend([
                f"👥 Группа 1 ID: {GROUP_CHAT_ID}",
                f"👥 Группа 2 ID: {GROUP_CHAT_ID_2}"
            ])
            
            if self.reminders:
                debug_msg.append("\n📋 ЗАГРУЖЕННЫЕ НАПОМИНАНИЯ:")
                for i, reminder in enumerate(sorted(self.reminders, key=lambda x: (x['date'], x['time'])), 1):
                    debug_msg.extend([
                        f"{i}. 📅 {reminder['date']} ⏰ {reminder['time'].strftime('%H:%M')}",
                        f"   📝 {reminder['message'][:40]}{'...' if len(reminder['message']) > 40 else ''}\n"
                    ])
            
            jobs = self.scheduler.get_jobs()
            if jobs:
                debug_msg.append("⏰ ЗАПЛАНИРОВАННЫЕ ЗАДАЧИ:")
                for i, job in enumerate(sorted(jobs, key=lambda x: x.next_run_time)[:5], 1):
                    debug_msg.append(f"{i}. {job.id} - {job.next_run_time}")
            
            await update.message.reply_text("\n".join(debug_msg))
            logger.info(f"Пользователь {update.effective_user.id} запросил отладку")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка отладки: {e}")
            logger.error(f"❌ Ошибка отладки: {e}")

    async def check_excel_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /check"""
        try:
            await update.message.reply_text("🔍 Проверяю Excel файл...")
            logger.info(f"Пользователь {update.effective_user.id} проверяет Excel файл")
            
            df = self.safe_read_excel()
            if df is None:
                await update.message.reply_text("❌ Не удалось прочитать файл!")
                return
            
            check_msg = [
                "📊 Проверка файла reminders.xlsx:\n",
                f"📋 Всего строк: {len(df)}",
                f"📝 Колонки: {', '.join(df.columns.tolist())}\n"
            ]
            
            for i, row in df.head(3).iterrows():
                date_str = str(row.get('Дата', ''))
                time_str = str(row.get('Время', row.get('Time', row.get('время', ''))))
                message = str(row.get('Сообщение', row.get('Message', row.get('сообщение', ''))))
                
                check_msg.extend([
                    f"Строка {i+1}:",
                    f"  📅 Дата: {date_str}",
                    f"  ⏰ Время: {time_str}",
                    f"  📝 Сообщение: {message[:30]}{'...' if len(message) > 30 else ''}\n"
                ])
                
            await update.message.reply_text("\n".join(check_msg))
            logger.info(f"Пользователь {update.effective_user.id} проверил Excel файл")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка проверки файла: {e}")
            logger.error(f"❌ Ошибка проверки файла: {e}")

    async def load_reminders_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /load"""
        try:
            await update.message.reply_text("📂 Загружаю напоминания из Excel...")
            logger.info(f"Пользователь {update.effective_user.id} загружает напоминания")
            
            self.reminders = self.read_reminders_from_excel()
            self.schedule_reminders()
            
            if self.reminders:
                await update.message.reply_text(f"✅ Загружено {len(self.reminders)} напоминаний!")
                
                info_msg = ["📋 Загруженные напоминания:\n"]
                for i, reminder in enumerate(sorted(self.reminders, key=lambda x: (x['date'], x['time']))[:5], 1):
                    info_msg.extend([
                        f"{i}. 📅 {reminder['date']} ⏰ {reminder['time'].strftime('%H:%M')}",
                        f"   📝 {reminder['message'][:40]}{'...' if len(reminder['message']) > 40 else ''}\n"
                    ])
                
                if len(self.reminders) > 5:
                    info_msg.append(f"... и еще {len(self.reminders) - 5} напоминаний")
                    
                await update.message.reply_text("\n".join(info_msg))
            else:
                await update.message.reply_text("⚠️ Напоминания не найдены. Проверьте файл reminders.xlsx")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка загрузки: {e}")
            logger.error(f"❌ Ошибка загрузки: {e}")

    async def list_reminders_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /list"""
        if not self.reminders:
            await update.message.reply_text("📋 Список напоминаний пуст. Используйте /load для загрузки.")
            return
            
        message = ["📋 Список напоминаний:\n"]
        for i, reminder in enumerate(sorted(self.reminders, key=lambda x: (x['date'], x['time'])), 1):
            message.extend([
                f"{i}. 📅 {reminder['date']} ⏰ {reminder['time'].strftime('%H:%M')}",
                f"   📝 {reminder['message'][:50]}{'...' if len(reminder['message']) > 50 else ''}\n"
            ])
            
        await update.message.reply_text("\n".join(message))

    async def reload_reminders_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /reload"""
        await self.load_reminders_command(update, context)

    async def time_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /time"""
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
        time_msg = f"🕐 Московское время: {moscow_time.strftime('%Y-%m-%d %H:%M:%S')}"
        await update.message.reply_text(time_msg)

    async def test_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /test"""
        await update.message.reply_text("🧪 Тест ОБНОВЛЕННОГО бота успешен!")
        
        try:
            try:
                test_message = (
                    "🧪 Тестовое сообщение от ОБНОВЛЕННОГО бота в группу 1!\n\n"
                    f"[График]({SPREADSHEET_URL}) Жми для просмотра"
                )
                await self.application.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=test_message,
                    parse_mode='Markdown'
                )
                await update.message.reply_text("✅ Тестовое сообщение отправлено в группу 1!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка отправки в группу 1: {e}")
            
            try:
                test_message = (
                    "🧪 Тестовое сообщение от ОБНОВЛЕННОГО бота в группу 2!\n\n"
                    f"[График]({SPREADSHEET_URL}) Жми для просмотра"
                )
                await self.application.bot.send_message(
                    chat_id=GROUP_CHAT_ID_2,
                    text=test_message,
                    parse_mode='Markdown'
                )
                await update.message.reply_text("✅ Тестовое сообщение отправлено в группу 2!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка отправки в группу 2: {e}")
            
            logger.info(f"Пользователь {update.effective_user.id} выполнил тест")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Общая ошибка теста: {e}")
            logger.error(f"❌ Общая ошибка теста: {e}")

    async def send_message_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /send"""
        try:
            moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
            message = f"📢 Тестовое сообщение от ОБНОВЛЕННОГО бота!\n🕐 Время: {moscow_time.strftime('%H:%M:%S')}"
            
            try:
                await self.application.bot.send_message(
                    chat_id=GROUP_CHAT_ID,
                    text=message
                )
                await update.message.reply_text("✅ Сообщение отправлено в группу 1!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка отправки в группу 1: {e}")
            
            try:
                await self.application.bot.send_message(
                    chat_id=GROUP_CHAT_ID_2,
                    text=message
                )
                await update.message.reply_text("✅ Сообщение отправлено в группу 2!")
            except Exception as e:
                await update.message.reply_text(f"❌ Ошибка отправки в группу 2: {e}")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка отправки: {e}")

    async def start_bot(self):
        """Запуск бота"""
        try:
            logger.info("🚀 Запуск ОБНОВЛЕННОГО бота...")
            
            # Загружаем напоминания при запуске
            self.reminders = self.read_reminders_from_excel()
            self.schedule_reminders()
            
            # Запускаем планировщик
            self.scheduler.start()
            logger.info("✅ Планировщик запущен")
            
            # Запускаем бота
            await self.application.run_polling()
            
        except Exception as e:
            logger.error(f"❌ Ошибка запуска бота: {e}")

    def run(self):
        """Запуск бота"""
        asyncio.run(self.start_bot())


if __name__ == "__main__":
    bot = FinalWorkingReminderBot()
    bot.run()
