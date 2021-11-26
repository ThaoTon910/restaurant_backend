import datetime

import requests
import os
import codecs
import json

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_URL = 'http://localhost:8080/v0'

def create_promotion_type(merchant_name: str):
    about_file = os.path.join(CURRENT_DIR, merchant_name, 'promotion_types.json')
    with open(about_file, 'r') as fp:
        about = json.load(fp)
        print(about)
        for type in about:
            r = requests.post(BASE_URL + '/promotiontype', json=type)
            if (r.status_code == 500):
                print(r.text)

if __name__ == "__main__":
    create_promotion_type("pho21")
