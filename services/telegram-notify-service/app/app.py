import logging
import config

from kombu import Message
from time import sleep

from broker import Broker
from telegram import TelegramAPI

# setup logging
logger = logging.getLogger("telegram-notify-service")
logging.basicConfig(
    level=logging.INFO,            
    format="[%(levelname)s][%(name)s][%(filename)s, line %(lineno)d]: %(message)s"
)

app_config: config.Config = config.load_config(_env_file='.env')
api = TelegramAPI(app_config.TELEGRAM_BOT_TOKEN.get_secret_value())

logging.info(f"Config loaded: {app_config}")
broker = Broker(
    ampq_dsn=app_config.RABBITMQ_DSN.unicode_string(),
    exchange_name=app_config.EXCHANGE_NAME,
    queue_name=app_config.QUEUE_NAME
)

def process_message(body, message: Message):
    logger.info(f"Recieved message {message} with content: {body}")

    try:
        for tele_id in app_config.TELEGRAM_CHAT_IDS:
            api.send_message_to_user(tele_id, body)
    finally:
        message.ack() #close message anyway

broker.register_callback(process_message)


def test(msg):
    broker.send_message(msg)


if __name__ == "__main__":
    logger.info(f"Loaded bot {api.getMe()}")

    #you can it test by
    # from threading import Timer
    # t = Timer(1, test, args=["message test"])
    # t.start()

    while True:
        try:
            broker.run_consumer()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt. Exiting...")
            break
        except Exception as e:
            logger.error(f"Connection error: {str(e)}. Retrying in 5 seconds...")
            sleep(5)

    