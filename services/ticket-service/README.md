# Ticket service

## Setting up
Set up your PosgreSQL in deploy folder

Create .env file in current folder with your data:
```ini
PG_DSN = "postgresql://LOGIN:PASSWORD@IP:PORT/DBNAME"
```
or use
```bash
export PG_DSN="postgresql://LOGIN:PASSWORD@IP:PORT/DBNAME"
```

## Settings loading order:
1. .env file
2. Environment
3. Default fields

## Running
```bash
source run.sh
```
or
```bash
uvicorn app.app:app --port 5000 --reload
```

Documentation: `http://localhost:5000/docs`

## Methods
| Method | Route | Description |
| --- | --- | --- |
| `get` | `tickets/` | Get all tickets |
| `post` | `tickets/` | Add new ticket |
| `get` | `tickets/{ticketID}` | Get ticket by ID |
| `delete` | `tickets/{ticketID}` | Delete ticket by ID |
| `put` | `tickets/{ticketID}` | Update ticket info by ID |
| `get` | `message/{messageID}` | Get message by ID |
| `put` | `message/{messageID}` | Update message by ID |
| `delete` | `message/{messageID}` | Delete message by ID |