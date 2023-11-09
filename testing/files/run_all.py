from subprocess import run
from threading import Timer

def run_all():
    run(["python3", "-m", "unittest", "files/e2e_test.py"])

if __name__ == "__main__":
    tim = Timer(20, run_all) #wait 10 seconds to start after all services
    tim.start()