import requests
import os
from dotenv import load_dotenv
load_dotenv()

MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN')

def send_mailgun_email(to, subject, text):
    url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    return requests.post(
        url,
        auth=("api", MAILGUN_API_KEY),
        data={"from": f"noreply@{MAILGUN_DOMAIN}", "to": to, "subject": subject, "text": text}
    )
