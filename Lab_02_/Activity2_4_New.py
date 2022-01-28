#Written by Savindu9x
#Last modified on 22/08/2021

#Importing required libraries
import Adafruit_DHT
import requests
import time
import RPi.GPIO as GPIO
import filestack

#set the sensor type
sensor = Adafruit_DHT.AM2302
#Set GPIO pin for data_in
GPIO.setmode(GPIO.BOARD)
GPIO=4


#define global variables
iter = 1 #make it 20

#function for sending text to private IFFT chat in Telegram
def send_text(avg_temp, avg_hum):
    print("Sending to Telegram...")
    #convert int to string literals
    data_string = "Average Temperature: " + str(avg_temp) + "\nAverage Humidity: " + str(avg_hum)
    #Post a request with API key and relavent value field
    r = requests.post("https://maker.ifttt.com/trigger/send_text/with/key/dnoW4eyZ1pL-VgPXKgGHOS", json = {"value1":data_string})
    if r.status_code == 200: #return code if successful
        print("Message Sent Successfully")
    else:
        print("Error!!")
        
def send_alert():
    print("Sending to Telegram...")
    #convert int to string literals
    data_string = "Temperature is above 50C degree"
    #Post a request with API key and relavent value field
    r = requests.post("https://maker.ifttt.com/trigger/send_text/with/key/dnoW4eyZ1pL-VgPXKgGHOS", json = {"value1":data_string})
    if r.status_code == 200: #return code if successful
        print("Message Sent Successfully")
    else:
        print("Error!!")
    

def main():
    tot_temp = 0
    tot_hum = 0
    #for loop runs for number data required to collect.
    for count in range(iter):
        #Take the temp and humidity readings
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO)
        if humidity is not None and temperature is not None: #if not Null
            print('Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
            print('\nSending Temperature data to ThingSpeak') #sends temperature data to thinkspeak field 01
            RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=2GL5ZPVB5XSR2KHG&field1='
            RequestToThingspeak += str(temperature)
            request = requests.get(RequestToThingspeak)
            print('data field 1 sent \n')
            time.sleep(15)
            print('Sending humidity data to ThingSpeak')  #sends humidity data to thinkspeak field 02
            RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=2GL5ZPVB5XSR2KHG&field2='
            RequestToThingspeak += str(temperature)
            request = requests.get(RequestToThingspeak)
            print('data field 2 sent \n')
            time.sleep(15)
            tot_temp += temperature #calculate total temperature for average
            tot_hum += humidity #calculate total humidity for average
        else: #raise an exception
            print("Failed to get reading. Try Again")
        #set time interval of 2 seconds for sensor to settle
        time.sleep(2)
    #calculate the average upto two decimels
    avg_temp = round(tot_temp/iter, 3)
    avg_hum = round(tot_hum/iter, 3)
    if avg_temp > 50:
        send_alert()
    
    #execute function to send the text
    send_text(avg_temp,avg_hum)
    

if __name__ == '__main__':
    main()