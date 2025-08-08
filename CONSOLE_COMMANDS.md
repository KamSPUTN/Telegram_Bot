# Команды для запуска бота через консоль на PythonAnywhere

## 1. Запуск через Always-on Task (Рекомендуется)

Если у вас уже настроен Always-on Task, бот запускается автоматически. Для проверки статуса:

```bash
# Проверить логи Always-on Task
tail -f pythonanywhere_bot.log
```

## 2. Запуск через консоль вручную

### Переход в директорию проекта:
```bash
cd ~/TelegramBot
```

### Проверка наличия файлов:
```bash
ls -la
```

### Запуск бота через основной скрипт:
```bash
python pythonanywhere_bot.py
```

### Альтернативный запуск через run_bot.py:
```bash
python run_bot.py
```

### Прямой запуск основного файла бота:
```bash
python reminder_bot_final_working_fixed_v13.py
```

## 3. Запуск в фоновом режиме

### Использование nohup:
```bash
nohup python pythonanywhere_bot.py > bot_output.log 2>&1 &
```

### Использование screen:
```bash
screen -S bot
python pythonanywhere_bot.py
# Нажмите Ctrl+A, затем D для отключения от screen
```

### Возврат к screen сессии:
```bash
screen -r bot
```

## 4. Мониторинг работы бота

### Просмотр логов в реальном времени:
```bash
tail -f pythonanywhere_bot.log
```

### Просмотр последних 50 строк логов:
```bash
tail -50 pythonanywhere_bot.log
```

### Проверка процессов Python:
```bash
ps aux | grep python
```

## 5. Остановка бота

### Если запущен в консоли:
Нажмите `Ctrl+C`

### Если запущен в фоне:
```bash
# Найти PID процесса
ps aux | grep python

# Остановить процесс
kill <PID>
```

### Если запущен в screen:
```bash
screen -r bot
# Затем Ctrl+C
```

## 6. Обновление бота

### Остановить текущий процесс
### Загрузить новый файл через Files
### Перезапустить:
```bash
python pythonanywhere_bot.py
```

## Примечания:

- **Always-on Task** - самый надежный способ для постоянной работы
- **Консольный запуск** - подходит для тестирования и отладки
- **Фоновый режим** - бот продолжит работать после закрытия консоли
- Всегда проверяйте логи для диагностики проблем
