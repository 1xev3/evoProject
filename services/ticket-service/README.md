# Ticket service

# Settings

### Setting up (If you not using Docker)
Set up your PosgreSQL

Create `.env` file in current folder with your data:
```ini
PG_DSN=postgresql://admin:admin_pass@localhost:PORT/mydb
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
uvicorn app.app:app --port 5000 --reload
```

## If you are using docker:

### Building from Dockerfile
Build service by using:
```bash
docker build -t "ticket-service:1.0" .
```

Configure your docker-compose file in `deploy` folder and run command:
```bash
docker-compose up -d
```



# Methods
Documentation: `http://localhost:5000/docs`
| Method | Route | Description |
| --- | --- | --- |
| `get` | `tickets/` | Get all tickets |
| `post` | `tickets/` | Add new ticket |
| `get` | `tickets/{ticketID}` | Get ticket by ID |
| `delete` | `tickets/{ticketID}` | Delete ticket by ID |
| `put` | `tickets/{ticketID}` | Update ticket info by ID |
| `get` | `tickets/messages/{messageID}` | Get message by ID |
| `put` | `tickets/messages/{messageID}` | Update message by ID |
| `delete` | `tickets/messages/{messageID}` | Delete message by ID |