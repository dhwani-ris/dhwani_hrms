import frappe
import requests


def generate_token():
    url = "https://login.keka.com/connect/token"

    payload = "grant_type=kekaapi&scope=kekaapi&client_id=769bd909-435c-4236-ad79-570f6dadd6fc&api_key=24ozE2teQrWnr-NuDFw1xqeZzipWBP_-TEB97QvxQwE%3D&client_secret=W9m4WFQIRlEKLZvio85a"
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded",
        "Cookie": "TiPMix=66.3598722673583; x-ms-routing-name=self",
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")
