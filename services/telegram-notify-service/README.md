# Telegram notify service

# Settings

### Setting up (If you not using Docker)
Create `.env` file in current folder with your data:
```ini
RABBITMQ_DSN=amqp://admin:admin_pass@localhost:5672//
TELEGRAM_CHAT_IDS=["YOUR_TELEGRAM_ID"]
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
```
Optional fields:
```ini
EXCHANGE_NAME=EXCHANGE_NAME
QUEUE_NAME=QUEUE_NAME
```

### Settings loading order:
1. .env file
2. Environment
3. Default fields

# Running
## Standalone:
```bash
source run.sh
```
or
```bash
python3 app/app.py
```

## If you are using docker:

### Building from Dockerfile
Build service by using:
```bash
docker build -t "telegram-notify-service:1.0" .
```

Configure your docker-compose file in `deploy` folder and run command:
```bash
docker-compose up -d
```

## Usage
Send message to your RabbitMQ