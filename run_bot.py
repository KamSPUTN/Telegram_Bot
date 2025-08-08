#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота на сервере
"""

import sys
import os
import logging
from datetime import datetime
import pytz

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('server_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Имя основного файла бота
BOT_FILE = 'reminder_bot_final_working_fixed_v12.py'

def main():
    """Главная функция запуска бота"""
    try:
        # Проверяем наличие необходимых файлов
        required_files = [BOT_FILE, 'reminders.xlsx', 'requirements.txt']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            logger.error(f"❌ Отсутствуют необходимые файлы: {missing_files}")
            return False
        
        # Показываем московское время
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
        logger.info(f"🚀 Запуск ОБНОВЛЕННОГО бота v12 на сервере: {moscow_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Импортируем и запускаем бота
        sys.path.append(os.path.dirname(os.path.abspath(BOT_FILE)))
        module_name = os.path.splitext(BOT_FILE)[0]
        bot_module = __import__(module_name)
        
        bot = bot_module.FinalWorkingReminderBot()
        logger.info("✅ Бот успешно импортирован")
        
        bot.run()
        
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Ошибка запуска бота: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)