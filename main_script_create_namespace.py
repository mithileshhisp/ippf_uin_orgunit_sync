import requests
import logging, datetime
import json
from dotenv import load_dotenv
import os
load_dotenv()
import requests
#from requests.auth import HTTPBasicAuth

DHIS2_GET_API_URL = os.getenv("DHIS2_GET_API_URL")
DHIS2_GET_USER = os.getenv("DHIS2_GET_USER")
DHIS2_GET_PASSWORD = os.getenv("DHIS2_GET_PASSWORD")

#print(DHIS2_GET_API_URL) 
#https://links.hispindia.org/ippf_uin/api/dataStore/accuityResponse/g2e5lEB62la
#https://links.hispindia.org/ippf_uin/api/dataStore/accuityResponse
#T77VMiQPJER  g2e5lEB62la xqVU0gGzpXp gRciStNaUPS Uga6HNayg9p uobrC4O3IB1
# ddqMj4ZCqDR Esr1RH0YAkB IoX9fRYL284 htfzdE441iT pFflz8ehXdK
tei_uid = "uobrC4O3IB1"
namespace_url = f"{DHIS2_GET_API_URL}dataStore/accuityResponse/{tei_uid}"

data = {
    "test": "hello"
}

session = requests.Session()
session.auth = (DHIS2_GET_USER, DHIS2_GET_PASSWORD)

print("Final URL:", namespace_url)

#response = session.post(namespace_url, json=data)
response = session.delete(namespace_url)

print(response.status_code)
print(response.text)


# https://links.hispindia.org/ippf_uin/api/dataStore/accuityResponse/T77VMiQPJER
#https://links.hispindia.org/ippf_uin/api/dataStore/accuityResponse/g2e5lEB62la
# https://links.hispindia.org/ippf_uin/api/dataStore/accuityResponse
