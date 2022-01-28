import RPi.GPIO as GPIO
import time
import requests  # Please install with PIP: pip install requests

request = None

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    PIN_TRIGGER_1 = 18
    PIN_ECHO_1 = 16

    GPIO.setup(PIN_TRIGGER_1, GPIO.OUT)
    GPIO.setup(PIN_ECHO_1, GPIO.IN)
    distance_2 = 0
    GPIO.output(PIN_TRIGGER_1, GPIO.LOW)

    for count in range(300):
        print("Waiting for sensor to settle")
        print("\n")
        time.sleep(2)
        print("Calculating distance")

        GPIO.output(PIN_TRIGGER_1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER_1, GPIO.LOW)

        while GPIO.input(PIN_ECHO_1) == 0:
            pulse_start_time_1 = time.time()
        while GPIO.input(PIN_ECHO_1) == 1:
            pulse_end_time_1 = time.time()

        pulse_duration_1 = pulse_end_time_1 - pulse_start_time_1
        distance_1 = round(pulse_duration_1 * 17150, 2)
        print("Distance:", distance_1, "cm")

        print('Sending to 1 ThingSpeak')

        RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=2GL5ZPVB5XSR2KHG&field1='
        RequestToThingspeak += str(distance_1)
        request = requests.get(RequestToThingspeak)

        diff = round(distance_1 - distance_2, 3)
        distance_2 = distance_1
        print(request.text)
        time.sleep(15)
        print('Sending to 2 ThingSpeak')

        RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=2GL5ZPVB5XSR2KHG&field2='
        RequestToThingspeak += str(diff)
        request = requests.get(RequestToThingspeak)
        print('distance difference:', diff, 'cm')
        time.sleep(15)
        print('')

finally:
    GPIO.cleanup()
