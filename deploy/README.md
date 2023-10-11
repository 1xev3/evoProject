# Deploy

### Build each service with:
```bash
docker build -t "SERVICE_NAME:VERSION"
```

### Environment & running
1. Create `.env` file in current directory.
2. Fill it with following data:
```ini
POSTGRES_USER=your_data
POSTGRES_PASSWORD=your_data
POSTGRES_DB=your_data
PG_DSN=postgresql://your_data:your_data@your_data:your_data/your_data
MONGO_USER=your_data
MONGO_PASSWORD=your_data
MINIO_ROOT_USER=your_data
MINIO_ROOT_PASSWORD=your_data
MINIO_DNS=your_ip:your_port
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