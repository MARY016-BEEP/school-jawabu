import os
import base64
import requests

from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


CONSUMER_KEY = os.getenv(
    "MPESA_CONSUMER_KEY"
)

CONSUMER_SECRET = os.getenv(
    "MPESA_CONSUMER_SECRET"
)

SHORTCODE = os.getenv(
    "MPESA_SHORTCODE"
)

PASSKEY = os.getenv(
    "MPESA_PASSKEY"
)

CALLBACK_URL = os.getenv(
    "MPESA_CALLBACK_URL"
)

ENVIRONMENT = os.getenv(
    "MPESA_ENVIRONMENT",
    "sandbox"
)


def get_base_url():

    if ENVIRONMENT == "production":

        return "https://api.safaricom.co.ke"

    return "https://sandbox.safaricom.co.ke"


def get_access_token():

    url = (
        f"{get_base_url()}"
        "/oauth/v1/generate?grant_type=client_credentials"
    )

    response = requests.get(

        url,

        auth=(
            CONSUMER_KEY,
            CONSUMER_SECRET
        ),

        timeout=30
    )

    response.raise_for_status()

    return response.json().get(
        "access_token"
    )


def generate_password():

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    raw_password = (
        str(SHORTCODE)
        + str(PASSKEY)
        + timestamp
    )

    password = base64.b64encode(
        raw_password.encode()
    ).decode()

    return password, timestamp


def format_phone_number(phone):

    phone = str(phone).strip()

    if phone.startswith("0"):

        return "254" + phone[1:]

    if phone.startswith("+254"):

        return phone[1:]

    return phone


def send_stk_push(

    phone_number,

    amount,

    registration_number

):

    token = get_access_token()

    password, timestamp = generate_password()

    url = (
        f"{get_base_url()}"
        "/mpesa/stkpush/v1/processrequest"
    )

    headers = {

        "Authorization":
        f"Bearer {token}",

        "Content-Type":
        "application/json"
    }

    phone = format_phone_number(
        phone_number
    )

    payload = {

        "BusinessShortCode":
        SHORTCODE,

        "Password":
        password,

        "Timestamp":
        timestamp,

        "TransactionType":
        "CustomerPayBillOnline",

        "Amount":
        int(amount),

        "PartyA":
        phone,

        "PartyB":
        SHORTCODE,

        "PhoneNumber":
        phone,

        "CallBackURL":
        CALLBACK_URL,

        "AccountReference":
        registration_number,

        "TransactionDesc":
        "JAWABU SCHOOL FEES"

    }

    response = requests.post(

        url,

        headers=headers,

        json=payload,

        timeout=30
    )

    response.raise_for_status()

    return response.json()