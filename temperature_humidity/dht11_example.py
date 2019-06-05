import RPi.GPIO as GPIO
import dht11
import time
import datetime

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

class TempReader:
    def __init__(self):
        print("Initializing Instance")
        self.instance = dht11.DHT11(pin=17)

    def getTemp(self):
        print("Getting Temperature")
        result = self.instance.read()
        while result.is_valid() != True:
            result = self.instance.read()
            time.sleep(1)

        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            print("Temperature: %d C" % result.temperature)
            print("Temperature: %d F" % ((result.temperature * 9/5) + 32))
            print("Humidity: %d %%" % result.humidity)
            fTemp = (result.temperature * 9/5) + 32.0
            rHumid = result.humidity


            #FIXME: Make this return cleaner
            #return str(Month-Day), str(Hour-Min), Temp(faren)
            return str(datetime.datetime.now().strftime("%m-%d")), str(datetime.datetime.now().strftime("%I:%M:%S")), str(fTemp), rHumid

        else:
            fTemp = "Error"
            return fTemp


class OldReader:
    def main():
        instance = dht11.DHT11(pin=17)
        while True:
            result = instance.read()
            if result.is_valid():
                print("Last valid input: " + str(datetime.datetime.now()))
                print("Temperature: %d C" % result.temperature)
                print("Temperature: %d F" % ((result.temperature * 9/5) + 32))
                print("Humidity: %d %%" % result.humidity)

            time.sleep(1)

if __name__ == '__main__':
    OldReader.main()
