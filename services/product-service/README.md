# Product service

# Settings

### Setting up (If you not using Docker)
Set up your MongoDB

Create `.env` file in current folder with your data:
```ini
MONGO_DSN = "mongodb://USER:PASSWORD@IP:PORT/tech-support"
```
or use in console before running
```bash
export MONGO_DSN="mongodb://USER:PASSWORD@IP:PORT/tech-support"
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
uvicorn app.app:app --port 5010 --reload
```

## If you are using docker:

### Building from Dockerfile
Build service by using:
```bash
docker build -t "product-service:1.0" .
```

Configure your docker-compose file in `deploy` folder and run command:
```bash
docker-compose up -d
```



# Methods
Documentation: `http://localhost:5010/docs`
| Method | Route | Description |
| --- | --- | --- |
| `TODO` | `TODO/` | TODO |