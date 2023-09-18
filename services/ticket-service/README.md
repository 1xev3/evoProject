# Ticket service

## Running
`uvicorn app.app:app --port 5000 --reload`

## Api
| Method | Route | Description |
| --- | --- | --- |
| `get` | `tickets/` | Get all tickets |
| `post` | `tickets/` | Add new ticket |
| `get` | `tickets/{ticketID}` | Get ticket by ID |
| `delete` | `tickets/{ticketID}` | Delete ticket by ID |
| `put` | `tickets/{ticketID}` | Update ticket info by ID |