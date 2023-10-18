# User service

### Environment
```ini
PG_DSN=postgresql+asyncpg://admin:admin_pass@localhost:5432/mydb
JWT_SECRET=JWT_SECRET
RESET_PASSWORD_TOKEN_SECRET=RESET_PASSWORD_TOKEN_SECRET
VERIFICATION_TOKEN_SECRET=VERIFICATION_TOKEN_SECRET
```

### Settings loading order:
1. .env file
2. Environment
3. Default fields

# Running
Script: `source run.sh`\
Uvicorn: `uvicorn app.app:app --port 5020 --reload`

# Building from Dockerfile
```bash
docker build -t "user-service:1.0" .
```

# Documentation
Will be awailable at: http://localhost:5020/docs
| Method | Route | Description |
| --- | --- | --- |
| POST | `groups/` | Create new group |
| GET | `groups/` | Get all groups |
| GET | `groups/{GroupID}` | Get group by ID |
| PUT | `groups/{GroupID}` | Update group by ID |
| DELETE | `groups/{GroupID}` | delete group by ID |