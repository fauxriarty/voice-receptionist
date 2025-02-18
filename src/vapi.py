import requests
from typing import Dict, Any, Optional
from .config import VAPI_API_KEY, VAPI_BASE_URL, PHONE_NUMBER_ID

def start_outbound_call(assistant_id: str, user_phone: str) -> Optional[str]:
    """
    triggers an outbound phone call to user_phone using the given assistant.
    returns a call id if successful.
    """
    url = f"{VAPI_BASE_URL}/call"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    # must specify type = outboundPhoneCall
    payload = {
        "type": "outboundPhoneCall",
        "name": "outbound call",
        "assistantId": assistant_id,
        "phoneNumberId": PHONE_NUMBER_ID,  # the 'from' number you created in vapi
        "customer": {
            "number": user_phone  # the 'to' number (must be e.164 format, e.g. +919930134457)
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        call_id = data.get("id")
        print('outbound call started with id:', call_id)
        return call_id
    except requests.RequestException as e:
        print('error starting outbound call:', e)
        if e.response is not None:
            print('response:', e.response.text)
        return None

def get_call_data(call_id: str) -> Dict[str, Any]:
    """
    fetches call details from vapi after the call completes.
    returns a dict containing call status, transcript, duration, etc.
    """
    url = f"{VAPI_BASE_URL}/call/{call_id}"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "call_id": call_id,
            "call_status": data.get("status", "unknown"),
            "ended_reason": data.get("endedReason", "none"),
            "duration": data.get("costBreakdown", {}).get("transport", 0),
            # might differ based on how vapi structures the data
            "transcript": data.get("artifact", {}).get("transcript", "")
        }
    except requests.RequestException as e:
        print('error fetching call data:', e)
        return {
            "call_id": call_id,
            "call_status": "error",
            "ended_reason": "unknown",
            "duration": 0,
            "transcript": ""
        }
