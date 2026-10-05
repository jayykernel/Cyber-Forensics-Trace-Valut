import csv
import json

def parse_mft_timeline(file_path):
    events = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append({
                "timestamp": row["Timestamp_UTC"],
                "source": "FileSystem (MFT)",
                "event": row["Action"],
                "description": f"{row['FilePath']} (User: {row['UserAccount']}) - {row['Notes']}",
                "reference": row["RecordID"]
            })
    return events
