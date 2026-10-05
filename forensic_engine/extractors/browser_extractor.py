import sqlite3
import json
from datetime import datetime, timedelta

def convert_webkit_time(webkit_timestamp):
    # WebKit epoch is Jan 1, 1601 UTC in microseconds
    epoch_start = datetime(1601, 1, 1)
    delta = timedelta(microseconds=webkit_timestamp)
    return (epoch_start + delta).strftime("%Y-%m-%d %H:%M:%S")

def parse_browser_artefacts(sqlite_path, cache_json_path):
    events = []

    # Process SQLite
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.visit_time, u.url, u.title, v.from_visit
        FROM visits v
        JOIN urls u ON v.url = u.id
    """)
    for row in cursor.fetchall():
        timestamp = convert_webkit_time(row["visit_time"])
        events.append({
            "timestamp": timestamp,
            "source": "Browser SQLite (Chrome)",
            "event": "Web Visit",
            "description": f"Visited URL: {row['url']} ({row['title']})",
            "reference": "chrome_history.sqlite - visits table"
        })
    conn.close()

    # Process metadata cache (exfil artifacts)
    with open(cache_json_path, "r", encoding="utf-8") as f:
        cache_data = json.load(f)
        for act in cache_data.get("FormUploadArtefacts", []):
            desc = f"Action: {act.get('Action')} to {act.get('Destination_URL')} - File: {act.get('Source_File_Path')} ({act.get('File_Size_Bytes')} bytes). Response ID: {act.get('Server_Response_JSON',{}).get('file_id')}"
            events.append({
                "timestamp": act["Timestamp_UTC"],
                "source": "Browser Cache/Metadata",
                "event": "Browser File Upload / Exfiltration",
                "description": desc,
                "reference": "chrome_cache_metadata.json"
            })

    return events
