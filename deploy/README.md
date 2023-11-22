# Deploy

### Environment & running
1. Create `.env` file in current directory.
2. Fill it with following data:
```ini
#PostgeSQL related
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin_pass
POSTGRES_DB=mydb
PG_DSN=postgresql://admin:admin_pass@postgresql:5432/mydb
PG_ASYNC_DSN=postgresql+asyncpg://admin:admin_pass@postgresql:5432/mydb

#MongoDB
MONGO_USER=admin
MONGO_PASSWORD=admin_pass
MONGO_DSN=mongodb://admin:admin_pass@mongo:27017/tech-support

#Minio
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=admin_pass
MINIO_DSN=minio:9000

#Secrets
JWT_SECRET=JWT_SECRET
RESET_PASSWORD_TOKEN_SECRET=RESET_PASSWORD_TOKEN_SECRET
VERIFICATION_TOKEN_SECRET=VERIFICATION_TOKEN_SECRET

#RabbitMQ
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=admin_pass
RABBITMQ_DSN=amqp://admin:admin_pass@rabbitmq:5672//

#Paths
DEFAULT_GROUPS_CONFIG_PATH=/mnt/default-groups.json
POLICIES_CONFIG_PATH=/mnt/policies.yaml

#Telegram related
TELEGRAM_CHAT_IDS=["PASTE_YOUR_USERID"]
TELEGRAM_BOT_TOKEN=PASTE_YOUR_BOTTOKEN
```

## NOTE - THIS SHOULD BE CONFIGURED BY YOURSELF!
```ini
TELEGRAM_CHAT_IDS=["PASTE_YOUR_USERID"] #can be obtained by GetMe bot in telegram
TELEGRAM_BOT_TOKEN=PASTE_YOUR_BOTTOKEN #can be registered from BotFather bot in telegram
```

3. Configure `docker-compose.yaml` if needed.
4. Run docker-compose:
(If first time):
```bash
docker-compose up --build
```

You can check logs by using: `docker-compose logs`\
To stop all services use:
```bash
docker-compose down
```