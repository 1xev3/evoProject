import unittest
import requests
import logging
import pydantic
from sqlalchemy import create_engine
from sqlalchemy.sql import text

from dotenv import load_dotenv
from os import environ
from typing import Any

#load .env file
load_dotenv(".env")

ENTRYPOINT = 'http://policy-enforcement-service:5100/'
DATABASE_DSN = environ.get("PG_DSN")
DATABASE_SCHEMA = "users"

ACCESS_DENIED_MESSAGE = {'message': 'Content not found'}
TICKET_DELETED_MESSAGE = { "message": "Ticket successfully deleted" }
ADMIN_GROUP_ID = 1
USER_GROUP_ID = 2

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-9s | %(message)s"
)

class User(pydantic.BaseModel):
    id: str 
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    nickname: str
    bio: str
    group_id: int

class Ticket(pydantic.BaseModel):
    creator_id: str
    caption: str
    status: int
    id: int
    messages: list[Any]

class TestCommonFunctionality(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_service_availability(self):
        response = requests.get(ENTRYPOINT+"/145gkajgsajgjg")
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

class BaseUserTestCase(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.test_user: User = None
        self.access_token: str = None

    def setUp(self, group_id: int) -> None:
        self._register_test_user(group_id)
        self._login()

    def tearDown(self) -> None:
        self._delete_test_user()

    def _register_test_user(self, group_id: int) -> User:
        payload = {
            "email": "test_user_example@example.com",
            "password": "password",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "nickname": "test",
            "bio": "test",
            "group_id": group_id
        }   
        try:
            logger.info("Running request")
            response = requests.post(f'{ENTRYPOINT}auth/register', json=payload) 
            response.raise_for_status()
            self.test_user = User(**response.json())
        except requests.exceptions.HTTPError as exc:
            logger.error(exc.response.text)
            logger.error(exc)

    def _raise_if_invalid_user(self):
        if self.test_user is None:
            raise Exception('Cannot continue test without valid user!')

    def _delete_test_user(self):
        if self.test_user is None:
            return
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(text(f"""DELETE FROM "{DATABASE_SCHEMA}"."user" WHERE id = '{self.test_user.id}';"""))
            connection.commit()

    def _set_superuser(self, is_superuser: bool):
        if self.test_user is None:
            return
        self.test_user.is_superuser = is_superuser
        engine = create_engine(DATABASE_DSN)
        with engine.connect() as connection:
            connection.execute(text(f"""UPDATE "{DATABASE_SCHEMA}"."user" SET is_superuser = {self.test_user.is_superuser} WHERE id = '{self.test_user.id}';"""))
            connection.commit()

    def _login(self):
        self._raise_if_invalid_user()
        try:
            data = {
                'username': 'test_user_example@example.com',
                'password': 'password',
            }
            response = requests.post(
                f'{ENTRYPOINT}auth/jwt/login', data=data
            ) 
            response.raise_for_status()
            self.access_token = response.json()['access_token']
        except requests.exceptions.HTTPError as exc:
            logger.error(exc)

    @property
    def auth_headers(self):  
        return {
            'Authorization': f'Bearer {self.access_token}'
        }  
         
class TestAdminPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(ADMIN_GROUP_ID)
        self._set_superuser(True)
        self._login()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}groups', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_create_delete_ticket(self):
        self._raise_if_invalid_user()
        
        payload = {
            "creator_id": self.test_user.id,
            "caption": "test_caption",
            "initial_message": "test message"
        }

        response = requests.post(f'{ENTRYPOINT}tickets', json=payload, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)

        #delete only for admin
        ticket = Ticket(**response.json())
        response = requests.delete(f'{ENTRYPOINT}tickets/{ticket.id}', json=payload, headers=self.auth_headers)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), TICKET_DELETED_MESSAGE)

class TestUserPolicies(BaseUserTestCase):
    def setUp(self) -> None:
        super().setUp(USER_GROUP_ID)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_groups_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}groups', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 404)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertDictEqual(data, ACCESS_DENIED_MESSAGE)

    def test_get_products_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}products', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_get_tickets_list(self):
        self._raise_if_invalid_user()
        response = requests.get(
            f'{ENTRYPOINT}tickets', headers=self.auth_headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()