#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота на PythonAnywhere
Специально адаптирован для работы в Always-on Tasks
"""

import sys
import os
import logging
from datetime import datetime
import pytz
import traceback

# Настройка логирования для PythonAnywhere
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('pythonanywhere_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Имя основного файла бота
BOT_FILE = 'reminder_bot_final_working_fixed_v13.py'

def main():
    """Главная функция запуска бота для PythonAnywhere"""
    try:
        # Показываем московское время
        moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
        logger.info(f"🚀 Запуск бота на PythonAnywhere: {moscow_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Проверяем наличие необходимых файлов
        required_files = [BOT_FILE, 'reminders.xlsx', 'requirements.txt']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            logger.error(f"❌ Отсутствуют необходимые файлы: {missing_files}")
            return False
        
        logger.info("✅ Все необходимые файлы найдены")
        
        # Импортируем и запускаем бота
        try:
            sys.path.append(os.path.dirname(os.path.abspath(BOT_FILE)))
            module_name = os.path.splitext(BOT_FILE)[0]
            bot_module = __import__(module_name)
            
            bot = bot_module.FinalWorkingReminderBot()
            logger.info("✅ Бот успешно импортирован")
            
            # Запускаем бота
            bot.run()
            
        except ImportError as e:
            logger.error(f"❌ Ошибка импорта модуля: {e}")
            logger.error(f"Полная ошибка: {traceback.format_exc()}")
            return False
        except Exception as e:
            logger.error(f"❌ Ошибка запуска бота: {e}")
            logger.error(f"Полная ошибка: {traceback.format_exc()}")
            return False
        
    except KeyboardInterrupt:
        logger.info("⏹️ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        logger.error(f"Полная ошибка: {traceback.format_exc()}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
