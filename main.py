
import threading
import time

from config import load_config

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting app')
    config = load_config()
    threads = []
    stop_event = threading.Event()
    try:
        dht1_settings = config['DHT1']

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
