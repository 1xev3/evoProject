# Tech-support

Project for `EvoAcademy`

# Services
| Service name | Path |
| --- | --- |
| Policy enforcement service | [Click](/services/policy-enforcement-service)
| User service | [Click](/services/user-service/)
| Product service | [Click](/services/product-service/)
| Ticket service | [Click](/services/ticket-service/)
| Review service | [Click](/services/review-service/)
| Telegram notify service | [Click](/services/telegram-notify-service/)

# Testing
e2e tests - [Click](/testing/) \
Telegram tests example - [Click](/services/telegram-notify-service/test)

# Checking for vulnerabilities

## Service vulnerabilities
1) Install bandit:
```sh
pip install bandit
```
2) Go to service:
```sh
cd /services/service-name
```
3) Check service with
```sh
python3 -m bandit -r ./app
```

## Docker image vulnerabilities
1) Install trivy
```sh
docker pull aquasec/trivy
```
2) Get all images from docker
```sh
docker images
```
3) Run check for image
```sh
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy image IMAGE_NAME
```

## Project diagram
![image](https://github.com/1xev3/evoProject/assets/53704889/406b3f41-c33c-4536-97df-84a317b2edc0)
