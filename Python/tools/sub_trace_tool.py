#tools/sub_trace_tool.py
import requests
from config import MIDAS_BASE_URL, VERIFY_SSL
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_traceability_data(userId: int, stationId: int, imei: str):
    # === getdpar ===
    dpar_resp = requests.post(
        f"{MIDAS_BASE_URL}/v3/getDparTraceability",
        json={"userId": userId, "stationId": stationId, "imei": imei},
        verify=VERIFY_SSL
    ).json()

    activities = []

    for entry in dpar_resp.get("data", []):
        txn_id = entry.get("mainInfo", {}).get("txnId")
        for tat in entry.get("tatInfo", []):
            if tat.get("type") == "ACTIVITY":
                activities.append({
                    "txnId": txn_id,
                    "activityName": tat.get("activityName"),
                    "activityDetailId": tat.get("activityDetailId"),
                })

    # === For each activity → ActivityDpar ===
    detailed_activities = []

    for act in activities:
        resp = requests.post(
            f"{MIDAS_BASE_URL}/v3/getDparTraceabilityActivityInfo",
            json={
                "txnId": act["txnId"],
                "activityDetailId": act["activityDetailId"],
                "activityName": act["activityName"],
            },
            verify=VERIFY_SSL
        ).json()
        detailed_activities.append(resp)

    # === ctdidpar ===
    ctdi_resp = requests.post(
        f"{MIDAS_BASE_URL}/ctdiDparTraceability",
        json={"userId": userId, "imei": imei},
        verify=VERIFY_SSL
    ).json()

    return {
        "activities": detailed_activities,
        "ctdi": ctdi_resp
    }
