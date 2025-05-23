import requests, os
from requests.auth import HTTPBasicAuth

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(url, auth=HTTPBasicAuth(os.getenv("CONSUMER_KEY"), os.getenv("CONSUMER_SECRET")))
    return r.json().get("access_token")
