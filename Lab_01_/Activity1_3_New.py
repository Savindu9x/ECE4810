import RPi.GPIO as GPIO
import time
import requests  # Please install with PIP: pip install requests

request = None

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    PIN_TRIGGER1 = 7
    PIN_ECHO1 = 11
    PIN_TRIGGER2 = 8
    PIN_ECHO2 = 10
    PIN_TRIGGER3 = 18
    PIN_ECHO3 = 16

    GPIO.setup(PIN_TRIGGER1, GPIO.OUT)
    GPIO.setup(PIN_ECHO1, GPIO.IN)
    GPIO.setup(PIN_TRIGGER2, GPIO.OUT)
    GPIO.setup(PIN_ECHO2, GPIO.IN)
    GPIO.setup(PIN_TRIGGER3, GPIO.OUT)
    GPIO.setup(PIN_ECHO3, GPIO.IN)

    GPIO.output(PIN_TRIGGER1, GPIO.LOW)
    GPIO.output(PIN_TRIGGER2, GPIO.LOW)
    GPIO.output(PIN_TRIGGER3, GPIO.LOW)

    for count in range(20):
        print("Waiting for sensor to settle")
        print("\n")
        print("Calculating US_1 distance")
        time.sleep(2)
        GPIO.output(PIN_TRIGGER1, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER1, GPIO.LOW)
        while GPIO.input(PIN_ECHO1) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO1) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:", distance, "cm")

        print('Sending to ThingSpeak')
        RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=2GL5ZPVB5XSR2KHG&field1='
        RequestToThingspeak += str(distance)
        request = requests.get(RequestToThingspeak)
        # print(request.text)
        time.sleep(15)
        print("first distance sent")
        print("\n")
        print("Calculating US_2 distance")
        GPIO.output(PIN_TRIGGER2, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER2, GPIO.LOW)
        while GPIO.input(PIN_ECHO2) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO2) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:", distance, "cm")

        print('Sending to ThingSpeak')
        RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=2GL5ZPVB5XSR2KHG&field2='
        RequestToThingspeak += str(distance)
        request = requests.get(RequestToThingspeak)
        # print(request.text)
        time.sleep(15)
        print("second distance sent")

        print("\n")
        print("Calculating US_3 distance")
        GPIO.output(PIN_TRIGGER3, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER3, GPIO.LOW)
        while GPIO.input(PIN_ECHO3) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO3) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:", distance, "cm")

        print('Sending to ThingSpeak')
        RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=2GL5ZPVB5XSR2KHG&field3='
        RequestToThingspeak += str(distance)
        request = requests.get(RequestToThingspeak)
        # print(request.text)
        time.sleep(15)
        print("Height sent")
        print("\n")

finally:
    GPIO.cleanup()





