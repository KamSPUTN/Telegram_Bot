# 🚀 Настройка Telegram бота на PythonAnywhere

## 📋 Шаг 1: Загрузка файлов на PythonAnywhere

1. **Откройте PythonAnywhere Dashboard**
2. **Перейдите в раздел "Files"**
3. **Создайте папку `TelegramBot`** в домашней директории
4. **Загрузите все файлы проекта:**
   - `reminder_bot_final_working_fixed_v12.py`
   - `pythonanywhere_bot.py`
   - `reminders.xlsx`
   - `requirements.txt`

## 📦 Шаг 2: Установка зависимостей

1. **Откройте Bash Console** на PythonAnywhere
2. **Перейдите в папку проекта:**
   ```bash
   cd ~/TelegramBot
   ```
3. **Установите зависимости:**
   ```bash
   pip install --user -r requirements.txt
   ```

## ⚙️ Шаг 3: Настройка Always-on Task

1. **Перейдите в раздел "Tasks"** на PythonAnywhere
2. **Нажмите "Add a new task"**
3. **Заполните форму:**

   **Command:**
   ```bash
   cd ~/TelegramBot && python pythonanywhere_bot.py
   ```

   **Schedule:** `daily` (или `hourly` для более частых проверок)

   **Enabled:** ✅ (поставьте галочку)

4. **Нажмите "Create"**

## 🔧 Шаг 4: Проверка работы

1. **Перейдите в раздел "Tasks"**
2. **Найдите вашу задачу и нажмите "Run now"**
3. **Проверьте логи** - они будут в файле `pythonanywhere_bot.log`

## 📊 Шаг 5: Мониторинг

### Просмотр логов:
```bash
cd ~/TelegramBot
tail -f pythonanywhere_bot.log
```

### Проверка статуса задачи:
- Перейдите в раздел "Tasks"
- Посмотрите на статус вашей задачи
- Если задача завершилась с ошибкой, нажмите "Run now" для перезапуска

## 🛠️ Шаг 6: Обновление бота

При обновлении кода:

1. **Загрузите новый файл бота** на PythonAnywhere
2. **Перейдите в раздел "Tasks"**
3. **Нажмите "Run now"** для перезапуска с новым кодом

## 🔍 Отладка проблем

### Если бот не запускается:

1. **Проверьте логи:**
   ```bash
   cd ~/TelegramBot
   cat pythonanywhere_bot.log
   ```

2. **Проверьте наличие файлов:**
   ```bash
   ls -la
   ```

3. **Проверьте зависимости:**
   ```bash
   pip list | grep -E "(telegram|pandas|apscheduler)"
   ```

### Частые проблемы:

- **ModuleNotFoundError:** Установите зависимости: `pip install --user -r requirements.txt`
- **PermissionError:** Проверьте права доступа к файлам
- **TokenError:** Проверьте правильность токена в коде

## ✅ Готово!

После настройки ваш бот будет:
- ✅ Работать 24/7
- ✅ Автоматически перезапускаться при ошибках
- ✅ Отправлять напоминания по расписанию
- ✅ Логировать все действия

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи в `pythonanywhere_bot.log`
2. Убедитесь, что все файлы загружены
3. Проверьте, что зависимости установлены
4. Перезапустите задачу в разделе "Tasks"
