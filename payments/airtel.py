import requests
import os
from dotenv import load_dotenv
load_dotenv()

AIRTEL_BASE_URL = os.getenv('AIRTEL_BASE_URL')
AIRTEL_CLIENT_ID = os.getenv('AIRTEL_CLIENT_ID')
AIRTEL_CLIENT_SECRET = os.getenv('AIRTEL_CLIENT_SECRET')

# Authentification OAuth2 pour Airtel Money

def get_airtel_access_token():
    url = f"{AIRTEL_BASE_URL}auth/oauth2/token"
    headers = {"Content-Type": "application/json"}
    data = {
        "client_id": AIRTEL_CLIENT_ID,
        "client_secret": AIRTEL_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    r = requests.post(url, json=data, headers=headers)
    return r.json().get('access_token')

# Paiement API (exemple)
def initiate_airtel_payment(msisdn, amount, reference):
    token = get_airtel_access_token()
    url = f"{AIRTEL_BASE_URL}merchant/v1/payments/"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "reference": reference,
        "subscriber": {"country": "GA", "currency": "XAF", "msisdn": msisdn},
        "transaction": {"amount": str(amount), "country": "GA", "currency": "XAF"}
    }
    r = requests.post(url, json=data, headers=headers)
    return r.json()
