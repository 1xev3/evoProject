# Deploy

### Build each service with:
```bash
docker build -t "SERVICE_NAME:VERSION"
```

### Environment & running
1. Create `.env` file in current directory.
2. Fill it with following data:
```ini
POSTGRES_USER=YOUR_USERNAME
POSTGRES_PASSWORD=YOUR_PASSWORD
POSTGRES_DB=YOUR_DATABASE_NAME
PG_DSN=postgresql://YOUR_USERNAME:YOUR_PASSWORD@YOUR_LOCAL_IP:PG_PORT/YOUR_DATABASE_NAME
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