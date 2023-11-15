# Review service

# Settings

### Setting up (If you not using Docker)
Set up your MongoDB, MinIO

Create `.env` file in current folder with your data:
```ini
PG_DSN=postgresql+asyncpg://admin:admin_pass@localhost:5432/mydb
RABBITMQ_DSN=amqp://admin:admin_pass@localhost:5672//
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
uvicorn app.app:app --port 5030 --reload
```

## If you are using docker:

### Building from Dockerfile
Build service by using:
```bash
docker build -t "review-service:1.0" .
```

Configure your docker-compose file in `deploy` folder and run command:
```bash
docker-compose up -d
```

# Methods
Documentation: `http://localhost:5030/docs`
| Method | Route | Description |
| --- | --- | --- |
| `get` | `reviews/` | Get all reviews |
| `post` | `reviews/` | Add new review |
| `get` | `reviews/{ReviewID}` | Get review by ID |
| `delete` | `reviews/{ReviewID}` | Delete review by ID |
| `get` | `reviews/{ReviewID}/likes` | Get all likes from review |
| `post` | `reviews/{ReviewID}/likes` | Upload new like to review |
| `delete` | `reviews/{ReviewID}/images&user_id` | Delete review like by UserID |