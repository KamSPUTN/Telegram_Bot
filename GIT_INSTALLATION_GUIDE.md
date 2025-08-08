# 📥 Установка Git и загрузка проекта в GitHub

## 🔧 Установка Git

### Для Windows:

1. **Скачайте Git для Windows:**
   - Перейдите на https://git-scm.com/download/win
   - Скачайте последнюю версию для Windows
   - Запустите установщик

2. **Настройка установки:**
   - Выберите "Use Git from Git Bash only" (рекомендуется)
   - Выберите "Use bundled OpenSSH"
   - Выберите "Use the OpenSSL library"
   - Выберите "Checkout as-is, commit Unix-style line endings"
   - Выберите "Use MinTTY"
   - Выберите "Default" для остальных опций

3. **Проверка установки:**
   ```bash
   git --version
   ```

### Альтернативная установка через Chocolatey:
```bash
choco install git
```

### Альтернативная установка через Winget:
```bash
winget install Git.Git
```

## 🔐 Настройка Git

### 1. Настройка пользователя:
```bash
git config --global user.name "Ваше Имя"
git config --global user.email "ваш.email@example.com"
```

### 2. Настройка SSH ключа (рекомендуется):
```bash
# Генерация SSH ключа
ssh-keygen -t ed25519 -C "ваш.email@example.com"

# Добавление ключа в SSH агент
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Копирование публичного ключа
cat ~/.ssh/id_ed25519.pub
```

### 3. Добавление ключа в GitHub:
- Перейдите в Settings → SSH and GPG keys
- Нажмите "New SSH key"
- Вставьте скопированный ключ

## 🚀 Загрузка проекта в GitHub

### Шаг 1: Инициализация репозитория
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

## 📋 Альтернативный способ загрузки

### Если Git не установлен, можно загрузить файлы через веб-интерфейс GitHub:

1. **Перейдите на https://github.com/KamSPUTN/Telegram_Bot**
2. **Нажмите "Add file" → "Upload files"**
3. **Перетащите все файлы проекта:**
   - `reminder_bot_final_working_fixed_v13.py`
   - `pythonanywhere_bot.py`
   - `run_bot.py`
   - `reminders.xlsx`
   - `requirements.txt`
   - `README.md`
   - `CONSOLE_COMMANDS.md`
   - `PYTHONANYWHERE_SETUP.md`
   - `PROJECT_CONTEXT.md`
   - `GITHUB_UPLOAD_GUIDE.md`
   - `.gitignore`
   - `LICENSE`

4. **Добавьте коммит сообщение:**
   ```
   Initial commit: Telegram Bot для напоминаний
   
   - Основной бот v13 с исправлениями
   - Скрипты для PythonAnywhere
   - Документация и инструкции
   - Excel файл с примерами данных
   - Полная настройка для развертывания
   ```

5. **Нажмите "Commit changes"**

## 🎯 Проверка загрузки

После загрузки проверьте на GitHub:
1. ✅ Все файлы загружены
2. ✅ README.md отображается корректно
3. ✅ .gitignore работает правильно
4. ✅ Структура проекта понятна
5. ✅ Документация полная

## 🔄 Обновления в будущем

### Через Git:
```bash
# Внести изменения
git add .
git commit -m "Описание изменений"
git push origin main
```

### Через веб-интерфейс:
1. Перейдите в нужный файл на GitHub
2. Нажмите на карандаш (Edit)
3. Внесите изменения
4. Добавьте описание изменений
5. Нажмите "Commit changes"

## 📞 Поддержка

Если возникнут проблемы:
1. Проверьте права доступа к репозиторию
2. Убедитесь, что Git настроен правильно
3. Проверьте подключение к интернету
4. Попробуйте загрузить файлы по одному через веб-интерфейс

## 🎉 Результат

После успешной загрузки ваш проект будет доступен по адресу:
**https://github.com/KamSPUTN/Telegram_Bot**

Другие разработчики смогут:
- Просматривать код
- Клонировать репозиторий
- Создавать Issues
- Делать Pull Requests
- Использовать проект в своих целях
