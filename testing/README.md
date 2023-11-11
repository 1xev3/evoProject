# e2e tests

## Environment
```ini
PG_DSN=postgresql://admin:admin_pass@localhost:5432/mydb
```

## Running
1. Create `.env` file with needed vars
2. Run: `source run.sh` OR run `docker-compose up --build` from `deploy/docker-compose`