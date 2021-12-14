import requests
import json
from datetime import datetime
import random
import time


def send_data(url, co2, temp, tvoc):#Todo Try catch
    payload = {'date': str(datetime.now().isoformat()),
               'co2': co2,
               'temp': temp,
               'tvoc': tvoc
               }

    # Create your header as required
    headers = {"content-type": "application/json"}


    print("Sending Message to Databse")
    try:
        r = requests.put(url, data=json.dumps(payload), headers=headers, timeout=10)
        print("Response: "+str(r.status_code))
    except Exception as e:
        print("Something went wrong: "+str(e))


def send_data_toggle(url, is_state):
    payload = {'state': is_state}

    # Create your header as required
    headers = {"content-type": "application/json"}

    print("Sending Message to Databse")
    try:
        r = requests.patch(url + '/windows/toggle/raspi', data=json.dumps(payload), headers=headers, timeout=10)
        print("Response: " + str(r.status_code))
    except Exception as e:
        print("Something went wrong: " + str(e))




