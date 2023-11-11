import os
import ast

from unittest import TestCase
from dotenv import load_dotenv

from app.telegram import TelegramAPI, schemas


load_dotenv(".env")

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_USER_IDS = ast.literal_eval(
    os.environ.get("TELEGRAM_USER_IDS")
)


class TelegramTestCase(TestCase):
    def setUp(self) -> None:
        self.api: TelegramAPI = TelegramAPI(TELEGRAM_BOT_TOKEN)

    def test_api_getMe(self):
        me = self.api.getMe()
        self.assertIsInstance(me, schemas.User)
        self.assertTrue(me.is_bot)

    def test_api_sendmsg(self):
        send_to = int(TELEGRAM_USER_IDS[0])

        msg = self.api.send_message_to_user(send_to, "test_message")
        self.assertIsInstance(msg, schemas.Message)
        self.assertTrue(msg.from_user.is_bot)
        self.assertEqual(msg.chat.id, send_to)
        self.assertEqual(msg.text, "test_message")

    def test_basic_get(self):
        check_from = int(TELEGRAM_USER_IDS[0])
        
        resp = self.api.get("getChat", {"chat_id": check_from})
        self.assertIsInstance(resp, schemas.BasicReponse)
        self.assertEqual(resp.result["id"], check_from)