# 🚀 Руководство по загрузке проекта в GitHub

## 📋 Подготовка к загрузке

### 1. Создание .gitignore файла
Сначала создайте файл `.gitignore` для исключения ненужных файлов:

```bash
# Создайте файл .gitignore в корне проекта
touch .gitignore
```

Содержимое `.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# Логи
*.log
bot_output.log

# Временные файлы Excel
~$*.xlsx
~$*.xls

# Системные файлы
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Резервные копии
*.bak
*.backup
```

### 2. Создание README.md для GitHub
Обновите существующий README.md или создайте новый:

```markdown
# 🤖 Telegram Bot для напоминаний

Telegram бот для автоматической отправки напоминаний на основе данных из Excel файла с интеграцией Google Sheets.

## ✨ Возможности

- 📅 Планирование напоминаний по дате и времени
- 📊 Чтение данных из Excel файла (`reminders.xlsx`)
- 🔗 Интеграция с Google Sheets
- 📱 Отправка в несколько Telegram групп
- ⏰ Автоматическое планирование с APScheduler
- 📝 Подробное логирование всех операций

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
└── PROJECT_CONTEXT.md                     # Контекст проекта
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

## 📊 Мониторинг

```bash
# Просмотр логов в реальном времени
tail -f pythonanywhere_bot.log

# Проверка процессов
ps aux | grep python
```

## 🛠️ Устранение неполадок

См. файл `PROJECT_CONTEXT.md` для подробной информации о решении проблем.

## 📄 Лицензия

MIT License

## 🤝 Поддержка

При возникновении проблем проверьте:
1. Логи бота
2. Формат данных в Excel файле
3. Настройки часового пояса
4. Доступность файлов
```

## 🔄 Пошаговая загрузка в GitHub

### Шаг 1: Инициализация Git репозитория
```bash
# В корневой папке проекта
git init
```

### Шаг 2: Добавление файлов
```bash
# Добавить все файлы (кроме исключенных в .gitignore)
git add .

# Проверить статус
git status
```

### Шаг 3: Первый коммит
```bash
git commit -m "Initial commit: Telegram Bot для напоминаний

- Основной бот v13 с исправлениями
- Скрипты для PythonAnywhere
- Документация и инструкции
- Excel файл с примерами данных
- Полная настройка для развертывания"
```

### Шаг 4: Подключение к GitHub
```bash
# Добавить удаленный репозиторий
git remote add origin https://github.com/KamSPUTN/Telegram_Bot.git

# Проверить подключение
git remote -v
```

### Шаг 5: Загрузка в GitHub
```bash
# Переименовать основную ветку (если нужно)
git branch -M main

# Загрузить в GitHub
git push -u origin main
```

## 📝 Дополнительные файлы для загрузки

### Создание LICENSE файла
Создайте файл `LICENSE` с MIT лицензией:

```text
MIT License

Copyright (c) 2025 KamSPUTN

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🎯 Финальная проверка

После загрузки проверьте на GitHub:
1. ✅ Все файлы загружены
2. ✅ README.md отображается корректно
3. ✅ .gitignore работает правильно
4. ✅ Структура проекта понятна
5. ✅ Документация полная

## 🔄 Обновления в будущем

Для обновления кода:
```bash
# Внести изменения
git add .
git commit -m "Описание изменений"
git push origin main
```

## 📞 Поддержка

Если возникнут проблемы с загрузкой:
1. Проверьте права доступа к репозиторию
2. Убедитесь, что Git настроен правильно
3. Проверьте подключение к интернету
4. Попробуйте загрузить файлы по одному
