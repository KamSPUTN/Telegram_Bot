# Контекст проекта: Telegram Bot для напоминаний

## 📋 Обзор проекта

**Цель:** Telegram бот для отправки напоминаний на основе данных из Excel файла с возможностью просмотра Google Sheets.

**Основные функции:**
- Чтение напоминаний из `reminders.xlsx`
- Планирование отправки по дате и времени
- Отправка в две группы Telegram
- Ссылка на Google Sheets в каждом сообщении
- Команды для управления (`/list`, `/check`, `/test`, `/load`)

## 🏗️ Архитектура

### Основные файлы:
- `reminder_bot_final_working_fixed_v13.py` - основной файл бота (актуальная версия)
- `pythonanywhere_bot.py` - скрипт для запуска на PythonAnywhere
- `run_bot.py` - альтернативный скрипт запуска
- `reminders.xlsx` - файл с данными напоминаний
- `requirements.txt` - зависимости Python

### Логи:
- `pythonanywhere_bot.log` - основной лог для PythonAnywhere
- `server_bot.log` - лог для серверного запуска
- `bot_final_working.log` - лог основного бота

## 🔧 Технические детали

### Зависимости:
```python
python-telegram-bot==20.7
pandas
openpyxl
apscheduler
watchdog
pytz
```

### Ключевые компоненты:
1. **Планировщик:** APScheduler с AsyncIOScheduler
2. **Триггеры:** DateTrigger для конкретных дат/времени
3. **Часовой пояс:** Europe/Moscow
4. **Форматирование:** Markdown для ссылок

### Структура Excel файла:
- **Дата** - дата напоминания
- **Время** - время напоминания  
- **Сообщение** - текст напоминания

## 🚀 Развертывание

### PythonAnywhere (основная платформа):
1. **Always-on Task** настроен для автоматического запуска
2. **Команда:** `cd ~/TelegramBot && python pythonanywhere_bot.py`
3. **Частота:** daily в 00:37

### Альтернативные способы запуска:
```bash
# Через консоль
python pythonanywhere_bot.py

# Прямой запуск
python reminder_bot_final_working_fixed_v13.py

# Фоновый режим
nohup python pythonanywhere_bot.py > bot_output.log 2>&1 &
```

## 📝 История изменений

### Версии бота:
- `v12` - исправлена ошибка парсинга `datetime.time`
- `v13` - добавлен текст "Жми для просмотра" после ссылки на Google Sheets

### Ключевые исправления:
1. **Проблема:** `TypeError: <class 'datetime.time'> is not convertible to datetime`
   **Решение:** Добавлена проверка `hasattr(time_str, 'hour')` в `read_reminders_from_excel`

2. **Проблема:** Напоминания отправлялись в неправильные даты
   **Решение:** Переход от `CronTrigger` к `DateTrigger` для точных дат

3. **Проблема:** Файл Excel недоступен при открытии локально
   **Решение:** Добавлена обработка ошибок и резервное копирование

## 🎯 Команды бота

### Пользовательские команды:
- `/list` - показать все загруженные напоминания
- `/check` - показать содержимое Excel файла
- `/test` - отправить тестовое сообщение
- `/load` - перезагрузить напоминания из Excel

### Административные:
- Автоматическая отправка напоминаний по расписанию
- Логирование всех операций
- Обработка ошибок с резервными копиями

## 🔗 Интеграции

### Telegram:
- **Группа 1:** Основная группа для напоминаний
- **Группа 2:** Дополнительная группа
- **Формат сообщений:** Markdown с ссылкой на Google Sheets

### Google Sheets:
- **URL:** https://docs.google.com/spreadsheets/d/1rojWrTFYKv0j06iSH7Aex9faEvDjbjYG/edit?gid=1984600935#gid=1984600935
- **Текст ссылки:** "График Жми для просмотра"

## 📊 Мониторинг

### Логирование:
```bash
# Просмотр в реальном времени
tail -f pythonanywhere_bot.log

# Последние записи
tail -50 pythonanywhere_bot.log
```

### Проверка процессов:
```bash
ps aux | grep python
```

## 🛠️ Устранение неполадок

### Частые проблемы:
1. **Пустой список `/list`** - проблема с парсингом времени
2. **Ошибки файла** - Excel открыт локально
3. **Неправильные даты** - проблема с часовыми поясами
4. **Бот останавливается** - нужно использовать Always-on Task

### Диагностика:
- Проверить логи: `tail -f pythonanywhere_bot.log`
- Проверить файлы: `ls -la ~/TelegramBot`
- Проверить процессы: `ps aux | grep python`

## 📁 Структура проекта

```
TelegramBot/
├── reminder_bot_final_working_fixed_v13.py  # Основной бот
├── pythonanywhere_bot.py                    # Скрипт для PythonAnywhere
├── run_bot.py                              # Альтернативный запуск
├── reminders.xlsx                          # Данные напоминаний
├── requirements.txt                        # Зависимости
├── pythonanywhere_bot.log                 # Основной лог
├── CONSOLE_COMMANDS.md                    # Команды запуска
├── PYTHONANYWHERE_SETUP.md               # Инструкции развертывания
└── PROJECT_CONTEXT.md                     # Этот файл
```

## 🎯 Текущий статус

**Актуальная версия:** `reminder_bot_final_working_fixed_v13.py`
**Платформа:** PythonAnywhere с Always-on Task
**Статус:** Работает стабильно
**Последнее обновление:** Добавлен текст "Жми для просмотра"

## 🔄 Процесс обновления

1. Загрузить новый файл через Files на PythonAnywhere
2. Остановить текущий процесс (если запущен в консоли)
3. Перезапустить Always-on Task
4. Проверить логи: `tail -f pythonanywhere_bot.log`

## 📞 Поддержка

При возникновении проблем:
1. Проверить логи
2. Убедиться в наличии всех файлов
3. Проверить формат данных в Excel
4. Перезапустить Always-on Task
