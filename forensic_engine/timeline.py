from datetime import datetime
import json

def is_suspicious_event(event):
    text = (event.get("event", "") + " " + event.get("description", "")).lower()
    suspicious_keywords = [
        "unauthorized", "stolen", "dvance", "dropfile", "tempmail",
        "proton", "exfiltration", "del /f", "del c:\\", "7z.exe a",
        "compress-archive", "file_delete", "usbstor", "sandisk", "rdp", "192.168.1.78"
    ]
    for kw in suspicious_keywords:
        if kw in text:
            return True
    return False

def generate_unified_timeline(all_events):
    # Standardize and sort
    def parse_time(item):
        t_str = item.get("timestamp", "1970-01-01 00:00:00")
        try:
            return datetime.strptime(t_str, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return datetime.min

    all_events.sort(key=parse_time)

    # Tag suspicious events
    for ev in all_events:
        ev["is_suspicious"] = is_suspicious_event(ev)

    return all_events
