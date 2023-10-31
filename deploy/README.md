# Deploy

### Build each service with:
```bash
docker build -t "SERVICE_NAME:VERSION"
```

### Environment & running
1. Create `.env` file in current directory.
2. Fill it with following data:
```ini
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin_pass
POSTGRES_DB=tech-support
PG_DSN=postgresql://admin:admin_pass@localhost:5432/tech-support
PG_ASYNC_DSN=postgresql+asyncpg://admin:admin_pass@localhost:5432/tech-support
MONGO_USER=admin
MONGO_PASSWORD=admin_pass
MONGO_DSN=mongodb://admin:admin_pass@localhost:27017/tech-support
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=admin_pass
MINIO_DSN=localhost:9000
JWT_SECRET=JWT_SECRET
RESET_PASSWORD_TOKEN_SECRET=RESET_PASSWORD_TOKEN_SECRET
VERIFICATION_TOKEN_SECRET=VERIFICATION_TOKEN_SECRET
POLICIES_CONFIG_PATH=/mnt/policies.yaml
RABBITMQ_DEFAULT_USER=admin
RABBITMQ_DEFAULT_PASS=admin_pass
RABBITMQ_DSN=amqp://admin:admin_pass@localhost:5672//
TELEGRAM_USER_IDS=["YOUR_TELEGRAM_ID"]
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_TOKEN
```
3. Configure `docker-compose.yaml` if needed.
4. Run docker-compose:
```bash
docker-compose up -d
```

You can check logs by using: `docker-compose logs`
To stop all services use:
```bash
docker-compose down
```