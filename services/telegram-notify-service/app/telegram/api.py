import requests
from logging import getLogger

from .schemas import HTTP_METHODS
from . import schemas

logger = getLogger("telegram-notify-service")

class TelegramAPI():
    def __init__(self, bot_token):
        self.base_url = f"https://api.telegram.org/bot{bot_token}"
    
    def __make_request(self, method: HTTP_METHODS, path:str, query:dict = None, payload: dict = None) -> schemas.BasicReponse:

        url = f"{self.base_url}/{path}"
        query_str = ""
        if query:
            query_str = '&'.join([f'{key}={value}' for key, value in query.items()])
            url = f"{url}?{query_str}"

        logger.info(f"Making request to {path} with query: {query}, payload:{payload}")
        if method == HTTP_METHODS.GET:
            response = requests.get(url)
        elif method == HTTP_METHODS.POST:
            response = requests.post(
                url, 
                json=payload, 
                headers={'Content-Type': 'application/json'}
            )
        else:
            raise ValueError("Unsupported HTTP method")
        
        if response.status_code != 200:
            logger.error(f"Request failed with status code {response.status_code}: {response.text}")
            raise requests.HTTPError(response=response)

        return schemas.BasicReponse(**response.json())
    
    def __get(self, path:str, query:dict = None):
        return self.__make_request(HTTP_METHODS.GET, path, query)
    
    def __post(self, path:str, query:dict = None, payload: dict = None):
        return self.__make_request(HTTP_METHODS.POST, path, query, payload)
    
    def getMe(self) -> schemas.User:
        resp = self.__get("getMe")
        return schemas.User(**resp.result)

    #https://core.telegram.org/method/messages.sendMessage
    def send_message_to_user(self, user_id, message) -> schemas.Message:
        payload = {"chat_id": user_id,"text": message}
        resp = self.__post("sendMessage", payload=payload).result

        msg = schemas.Message(
            message_id=resp["message_id"],
            from_user=schemas.User(**resp["from"]),
            chat=schemas.Chat(**resp["chat"]),
            date=resp["date"],
            text=resp["text"]
        )

        return msg

    