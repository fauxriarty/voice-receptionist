import requests
from typing import Dict, Any, Optional, Tuple
from .config import VAPI_API_KEY, VAPI_BASE_URL, PHONE_NUMBER_ID

def start_outbound_call(assistant_id: str, user_phone: str) -> Tuple[Optional[str], str]:
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
        # truncate the response text to first 300 chars
        resp_text = response.text
        truncated = resp_text[:300] + ("..." if len(resp_text) > 300 else "")
        debug_log.append(f"vapi response text (truncated): {truncated}")
        response.raise_for_status()
        data = response.json()
        call_id = data.get("id")
        debug_log.append(f"outbound call started with id: {call_id}")
        # final debug log
        return call_id, "\n".join(debug_log)
    except requests.RequestException as e:
        err_msg = f"error starting outbound call: {e}"
        debug_log.append(err_msg)
        if hasattr(e, "response") and e.response is not None:
            resp_text = e.response.text
            truncated = resp_text[:300] + ("..." if len(resp_text) > 300 else "")
            debug_log.append(f"response text (truncated): {truncated}")
        return None, "\n".join(debug_log)

def get_call_data(call_id: str) -> Tuple[Dict[str, Any], str]:
    debug_log = []
    url = f"{VAPI_BASE_URL}/call/{call_id}"
    headers = {"Authorization": f"Bearer {VAPI_API_KEY}"}
    debug_log.append(f"fetching call data for call_id: {call_id}")

    try:
        response = requests.get(url, headers=headers, timeout=10)
        debug_log.append(f"vapi response status: {response.status_code}")
        # truncate response text
        resp_text = response.text
        truncated = resp_text[:300] + ("..." if len(resp_text) > 300 else "")
        debug_log.append(f"vapi response text (truncated): {truncated}")

        response.raise_for_status()
        data = response.json()

        # parse additional fields
        started_at = data.get("startedAt", "")
        ended_at = data.get("endedAt", "")
        analysis_summary = data.get("analysis", {}).get("summary", "")
        recording_url = data.get("artifact", {}).get("recordingUrl", "")
        cost = data.get("cost", 0)  # total cost

        call_data = {
            "call_id": call_id,
            "call_status": data.get("status", "unknown"),
            "ended_reason": data.get("endedReason", "none"),
            "duration": data.get("costBreakdown", {}).get("transport", 0),
            "transcript": data.get("artifact", {}).get("transcript", ""),
            "started_at": started_at,
            "ended_at": ended_at,
            "analysis_summary": analysis_summary,
            "recording_url": recording_url,
            "cost": cost
        }

        debug_log.append(f"retrieved call data (parsed): {call_data}")
        return call_data, "\n".join(debug_log)
    except requests.RequestException as e:
        err_msg = f"error fetching call data: {e}"
        debug_log.append(err_msg)
        return {
            "call_id": call_id,
            "call_status": "error",
            "ended_reason": "unknown",
            "duration": 0,
            "transcript": "",
            "started_at": "",
            "ended_at": "",
            "analysis_summary": "",
            "recording_url": "",
            "cost": 0
        }, "\n".join(debug_log)
