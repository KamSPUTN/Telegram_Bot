# 🤖 Telegram Bot для напоминаний

Telegram бот для автоматической отправки напоминаний на основе данных из Excel файла с интеграцией Google Sheets.

## ✨ Возможности

- 📅 Планирование напоминаний по дате и времени
- 📊 Чтение данных из Excel файла (`reminders.xlsx`)
- 🔗 Интеграция с Google Sheets
- 📱 Отправка в несколько Telegram групп
- ⏰ Автоматическое планирование с APScheduler
- 📝 Подробное логирование всех операций
- 🌍 Поддержка часового пояса Europe/Moscow

## 🚀 Быстрый старт

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Настройка
1. Создайте бота через [@BotFather](https://t.me/BotFather)
2. Получите токен бота
3. Добавьте токен в переменную `BOT_TOKEN` в файле бота
4. Добавьте ID групп в переменные `GROUP_1_ID` и `GROUP_2_ID`

### Запуск
```bash
# Основной запуск
python reminder_bot_final_working_fixed_v13.py

# Для PythonAnywhere
python pythonanywhere_bot.py

# Альтернативный запуск
python run_bot.py
```

## 📁 Структура проекта

```
TelegramBot/
├── reminder_bot_final_working_fixed_v13.py  # Основной бот
├── pythonanywhere_bot.py                    # Скрипт для PythonAnywhere
├── run_bot.py                              # Альтернативный запуск
├── reminders.xlsx                          # Данные напоминаний
├── requirements.txt                        # Зависимости
├── README.md                              # Документация
├── CONSOLE_COMMANDS.md                    # Команды запуска
├── PYTHONANYWHERE_SETUP.md               # Инструкции развертывания
├── PROJECT_CONTEXT.md                     # Контекст проекта
└── GITHUB_UPLOAD_GUIDE.md                # Руководство по загрузке
```

## 🎯 Команды бота

- `/list` - показать все загруженные напоминания
- `/check` - показать содержимое Excel файла
- `/test` - отправить тестовое сообщение
- `/load` - перезагрузить напоминания из Excel

## 🔧 Технические детали

### Зависимости
- `python-telegram-bot==20.7`
- `pandas`
- `openpyxl`
- `apscheduler`
- `watchdog`
- `pytz`

### Платформы
- **Основная:** PythonAnywhere с Always-on Task
- **Альтернативная:** Любой сервер с Python 3.8+

### Структура Excel файла
- **Дата** - дата напоминания
- **Время** - время напоминания
- **Сообщение** - текст напоминания

## 📊 Мониторинг

```bash
# Просмотр логов в реальном времени
tail -f pythonanywhere_bot.log

# Проверка процессов
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

См. файл `PROJECT_CONTEXT.md` для подробной информации о решении проблем.

## 🔗 Интеграции

### Telegram:
- **Группа 1:** Основная группа для напоминаний
- **Группа 2:** Дополнительная группа
- **Формат сообщений:** Markdown с ссылкой на Google Sheets

### Google Sheets:
- **URL:** https://docs.google.com/spreadsheets/d/1rojWrTFYKv0j06iSH7Aex9faEvDjbjYG/edit?gid=1984600935#gid=1984600935
- **Текст ссылки:** "График Жми для просмотра"

## 📝 История версий

### v13 (Текущая)
- ✅ Добавлен текст "Жми для просмотра" после ссылки на Google Sheets
- ✅ Исправлена ошибка парсинга `datetime.time`
- ✅ Переход от `CronTrigger` к `DateTrigger` для точных дат
- ✅ Обработка ошибок при работе с Excel файлом

### v12
- ✅ Исправлена ошибка `TypeError: <class 'datetime.time'> is not convertible to datetime`
- ✅ Добавлена проверка `hasattr(time_str, 'hour')` в `read_reminders_from_excel`

## 📄 Лицензия

MIT License - см. файл `LICENSE`

## 🤝 Поддержка

При возникновении проблем проверьте:
1. Логи бота
2. Формат данных в Excel файле
3. Настройки часового пояса
4. Доступность файлов

## 🚀 Развертывание

Подробные инструкции по развертыванию на PythonAnywhere см. в файле `PYTHONANYWHERE_SETUP.md`

## 📞 Контакты

Проект создан для автоматизации отправки напоминаний с интеграцией Google Sheets. 