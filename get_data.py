import requests
import json
from datetime import datetime
import random
import time


def get_data(url):
    # Create your header as required
    headers = {"content-type": "application/json"}
    print("getting Tresholds from Databse")
    try:
        r = requests.get(url + '/windows', headers=headers, timeout=2)
        print("Response: " + str(r.status_code))
        return r.json()
    except Exception as e:
        print("Something went wrong: " + str(e))
        return None
