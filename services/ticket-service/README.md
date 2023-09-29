# Ticket service

## Setting up
- Set up your PosgreSQL in deploy folder
- Create .env file in folder `./app` with your data:
    - DATABASE_URL = "postgresql://LOGIN:PASSWORD@IP:PORT/DBNAME"
- Configure your venv: 
    - Add new venv: `python3 -m venv venv`
    - Activate: `source venv/bin/activate`
    - Install dependencies: `pip install -r requirements.txt`

## Running
- `source run.sh`

## Api
| Method | Route | Description |
| --- | --- | --- |
| `get` | `tickets/` | Get all tickets |
| `post` | `tickets/` | Add new ticket |
| `get` | `tickets/{ticketID}` | Get ticket by ID |
| `delete` | `tickets/{ticketID}` | Delete ticket by ID |
| `put` | `tickets/{ticketID}` | Update ticket info by ID |