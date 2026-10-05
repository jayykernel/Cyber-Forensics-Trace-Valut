import json

def parse_auth_logs(event_log_path, sys_reg_path):
    events = []

    with open(event_log_path, "r", encoding="utf-8") as f:
        log_data = json.load(f)
        for log in log_data:
            desc = log.get("Notes", "")
            if "TargetUserName" in log:
                desc += f" [User: {log['TargetUserName']}]"
            elif "SubjectUserName" in log:
                desc += f" [User: {log['SubjectUserName']}]"

            if "IpAddress" in log and log["IpAddress"]:
                desc += f" [IP: {log['IpAddress']}]"

            events.append({
                "timestamp": log["Timestamp_UTC"],
                "source": "Security EventLogs",
                "event": log["EventType"],
                "description": desc,
                "reference": f"EventID: {log.get('EventID')}"
            })

    with open(sys_reg_path, "r", encoding="utf-8") as f:
        reg_data = json.load(f)
        for act in reg_data.get("UserAssist_MRU", []):
            events.append({
                "timestamp": act["LastExecution_UTC"],
                "source": "Registry (UserAssist)",
                "event": "Program Execution",
                "description": f"Executed {act.get('Executable')} (RunCount: {act.get('RunCount')})",
                "reference": "NTUSER.DAT\\UserAssist"
            })

        for dev in reg_data.get("USBSTOR_Artifacts", []):
            events.append({
                "timestamp": dev["FirstInstallDate_UTC"],
                "source": "Registry (USBSTOR)",
                "event": "USB device inserted",
                "description": f"Device {dev.get('Vendor')} {dev.get('Product')} (Serial: {dev.get('SerialNumber')}) attached to {dev.get('AssignedDriveLetter')}",
                "reference": "HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR"
            })
            events.append({
                "timestamp": dev["LastRemovalDate_UTC"],
                "source": "Registry (USBSTOR)",
                "event": "USB device removed",
                "description": f"Device {dev.get('Vendor')} {dev.get('Product')} removed",
                "reference": "HKLM\\SYSTEM\\CurrentControlSet\\Enum\\USBSTOR"
            })

        for folder in reg_data.get("Shellbags_FolderAccess", []):
             events.append({
                "timestamp": folder["LastAccess_UTC"],
                "source": "Registry (Shellbags)",
                "event": "Folder Visited in Explorer",
                "description": f"Accessed {folder.get('FolderPath')} via GUI by {folder.get('AccessingUser')}",
                "reference": "NTUSER.DAT\\Shellbags"
            })

    return events
