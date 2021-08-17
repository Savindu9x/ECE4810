#written by Pasan Savindu Wickramarathna
#Last modified on 17-08-2021
# pip install requests
import requests
import time
import random

request = None

for count in range(3):
    RequestToThingspeak =  'https://api.thingspeak.com/update?api_key=YOUR_API_KEY&field1='
    RequestToThingspeak += str((random.randint(1,100)))
    request = requests.get(RequestToThingspeak)
    print(request.text)
    time.sleep(15)

