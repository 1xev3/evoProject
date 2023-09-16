# User service

## Running
`uvicorn app.app:app --port 5000 --reload`

## Api
| Method | Route | Description |
| --- | --- | --- |
| `get` | `users/` | Get all users |
| `post` | `users/` | Add new user |
| `get` | `users/{userID}` | Get user by ID |
| `delete` | `users/{userID}` | Delete user by ID |
| `put` | `users/{userID}` | Update userinfo by ID |