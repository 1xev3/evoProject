from subprocess import run
from threading import Timer
from logging import getLogger

logger = getLogger(__name__)

def run_all():
    run(["python3", "-m", "unittest", "files/policy_e2e.py"])
    run(["python3", "-m", "unittest", "files/product_e2e.py"])

if __name__ == "__main__":
    logger.info("Tests will run after 15 seconds")
    tim = Timer(15, run_all) #wait 15 seconds to start after all services
    tim.start()