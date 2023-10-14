# Product service

# Settings

### Setting up (If you not using Docker)
Set up your MongoDB, MinIO

Create `.env` file in current folder with your data:
```ini
MONGO_DSN = mongodb://USER:PASSWORD@IP:PORT/tech-support
MINIO_DSN=your_ip:your_port
MINIO_ACCESS_KEY=your_value
MINIO_SECRET_KEY=your_value
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
| `get` | `products/` | Get all products |
| `post` | `product/` | Add new product |
| `get` | `product/{ProductID}` | Get product by ID |
| `delete` | `product/{ProductID}` | Delete product by ID |
| `put` | `product/{ProductID}` | Update product by ID |
| `get` | `product/{ProductID}/image/{ImageUID}` | Download product image |
| `post` | `product/{ProductID}/image` | Upload new image to product |
| `delete` | `product/{ProductID}/image/{ImageUID}` | Delete product image by ID |