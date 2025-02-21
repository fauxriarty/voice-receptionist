import requests
from typing import Dict, Any, Optional, Tuple
from .config import VAPI_API_KEY, VAPI_BASE_URL, PHONE_NUMBER_ID

def start_outbound_call(assistant_id: str, user_phone: str) -> Tuple[Optional[str], str]:
    """
    triggers an outbound phone call to user_phone using the given assistant.
    returns a tuple of (call_id, debug_log).
    """
    debug_log = []
    url = f"{VAPI_BASE_URL}/call"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "outboundPhoneCall",
        "name": "outbound call",
        "assistantId": assistant_id,
        "phoneNumberId": PHONE_NUMBER_ID,
        "customer": {
            "number": user_phone
        }
    }

    debug_log.append(f"attempting outbound call with payload: {payload}")

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        debug_log.append(f"vapi response status: {response.status_code}")
        debug_log.append(f"vapi response text: {response.text}")

        response.raise_for_status()
        data = response.json()
        call_id = data.get("id")
        debug_log.append(f"outbound call started with id: {call_id}")
        return call_id, "\n".join(debug_log)
    except requests.RequestException as e:
        err_msg = f"error starting outbound call: {e}"
        debug_log.append(err_msg)
        if hasattr(e, "response") and e.response is not None:
            debug_log.append(f"response text: {e.response.text}")
        return None, "\n".join(debug_log)

def get_call_data(call_id: str) -> Tuple[Dict[str, Any], str]:
    """
    fetches call details from vapi after the call completes.
    returns a tuple of (call_data, debug_log).
    """
    debug_log = []
    url = f"{VAPI_BASE_URL}/call/{call_id}"
    headers = {
        "Authorization": f"Bearer {VAPI_API_KEY}"
    }
    debug_log.append(f"fetching call data for call_id: {call_id}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        debug_log.append(f"vapi response status: {response.status_code}")
        debug_log.append(f"vapi response text: {response.text}")

        response.raise_for_status()
        data = response.json()
        call_data = {
            "call_id": call_id,
            "call_status": data.get("status", "unknown"),
            "ended_reason": data.get("endedReason", "none"),
            "duration": data.get("costBreakdown", {}).get("transport", 0),
            "transcript": data.get("artifact", {}).get("transcript", "")
        }
        debug_log.append(f"retrieved call data: {call_data}")
        return call_data, "\n".join(debug_log)
    except requests.RequestException as e:
        err_msg = f"error fetching call data: {e}"
        debug_log.append(err_msg)
        return {
            "call_id": call_id,
            "call_status": "error",
            "ended_reason": "unknown",
            "duration": 0,
            "transcript": ""
        }, "\n".join(debug_log)
