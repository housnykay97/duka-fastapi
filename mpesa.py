import requests, base64, math
from datetime import datetime
from requests.auth import HTTPBasicAuth

consumer_key = 'lcWMDTdLr6WwQRubKRrGAmlAxwaOB2CcRgV0ArxsEsqYWsq0'
consumer_secret = 'LwvjRZQxGghuDJvVtUdyqRag6qSwrDZrFpSHVbQocMx7AnSDdBtHO9sD2UJ9AxTr'
saf_api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
saf_short_code = '174379'
saf_pass_key = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
saf_stkpush_api = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
my_callback_url = 'https://flattery-nemeses-bluish.ngrok-free.dev/saf-callback' #expires each time I restart ngrok and re-run the push


# Safaricom needs password first(A fresh password is generated each time because timestamp must be current)
def generate_password_and_timestamp():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = saf_short_code + saf_pass_key + timestamp
    password_bytes = password_str.encode()
    password = base64.b64encode(password_bytes).decode("utf-8")
    return password, timestamp


# sending consumer key and secret to get token
def get_mpesa_access_token():
    try:
        res = requests.get(
            saf_api_url,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
        )
        return res.json()['access_token']
    except Exception as e:
        print(str(e), "error getting access token")
        raise e


# This is where the actual charging takes place
def make_stk_push(payload):
    print(payload)
    amount_paid = payload['amount_paid']
    phone_number = payload['phone_number']
    sale_id = payload.get('sale_id')  

    # Dynamically generate token and password on every push
    token = get_mpesa_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    password, timestamp = generate_password_and_timestamp()

    push_data = {
        "BusinessShortCode": saf_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": math.ceil(float(amount_paid)),
        "PartyA": phone_number,
        "PartyB": saf_short_code,
        "PhoneNumber": phone_number,
        "CallBackURL": my_callback_url,
        "AccountReference": str(payload.get('sale_id')),
        "TransactionDesc": "description of the transaction",
    }

    response = requests.post(
        saf_stkpush_api,
        json=push_data,
        headers=headers)

    return response.json()