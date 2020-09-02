import RPi.GPIO as GPIO
import time

class LED:
    def __init__(self, channel):
        self.GPIO_num = channel
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(channel,GPIO.OUT)

    def on(self):
        print("LED ON")
        GPIO.output(self.GPIO_num, GPIO.HIGH)

    def off(self):
        print("LED OFF")
        GPIO.output(self.GPIO_num, GPIO.LOW)

    def on_off(self, timeToSleep):
        self.on()
        time.sleep(timeToSleep)
        self.off()

def main():
    red = LED(18)
    red.on_off(1)

    blue = LED(23)
    blue.on_off(1)

    white = LED(24)
    white.on_off(1)

    green = LED(25)
    green.on_off(1)

if __name__ == '__main__':
    main()
