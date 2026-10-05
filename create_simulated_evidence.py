import os
import sqlite3
import json
import csv
import hashlib

def create_evidence():
    base_dir = r"C:\dev\Trace-Valut\evidence"

    # 1. Victim Project Files
    proj_dir = os.path.join(base_dir, "filesystem", "victim_project")
    os.makedirs(proj_dir, exist_ok=True)

    drone_code = '''"""
Autonomous Drone Navigation Core - Proprietary Algorithm
Lead Researcher: Alex Mercer (CS-2026-8841)
Confidential - All Rights Reserved (C) 2026
"""

import numpy as np
import torch

class AutonomousDroneNavigator:
    def __init__(self, weights_path="neural_weights_v4.bin"):
        self.weights_path = weights_path
        self.lidar_resolution = 0.05
        self.collision_threshold = 0.35
        self.model = self._load_model()

    def _load_model(self):
        print(f"[NAV-CORE] Loading proprietary weights from {self.weights_path}")
        return {"architecture": "Transformer-Lidar-Hybrid-v4", "status": "initialized"}

    def compute_trajectory(self, lidar_pointcloud, velocity_vector):
        # Novel low-latency predictive path computation
        obstacle_density = np.mean(lidar_pointcloud > self.collision_threshold)
        optimal_vector = velocity_vector * (1.0 - obstacle_density)
        return optimal_vector

if __name__ == "__main__":
    nav = AutonomousDroneNavigator()
    print("[NAV-CORE] Autonomous Drone Navigation System Ready.")
'''
    with open(os.path.join(proj_dir, "drone_nav_core.py"), "w", encoding="utf-8") as f:
        f.write(drone_code)

    with open(os.path.join(proj_dir, "neural_weights_v4.bin"), "wb") as f:
        f.write(b"DRONE_AI_NEURAL_WEIGHTS_V4_TENSOR_DATA_MAGIC_0x9948AB" + b"\x00\x01\x02\x03" * 1024)

    with open(os.path.join(proj_dir, "dataset_lidar_final.parquet"), "wb") as f:
        f.write(b"PAR1_LIDAR_POINT_CLOUD_DATASET_FINAL_TEST_FLIGHT_OCT2026" + b"\xAA\xBB\xCC\xDD" * 2048)

    docx_text = """CONFIDENTIAL RESEARCH DISSERTATION & PATENT APPLICATION
Title: Real-Time Transformer-Based LiDAR Obstacle Avoidance for Autonomous UAVs
Author: Alex Mercer (Student ID: CS-2026-8841)
Advisor: Prof. Robert Hall, Department of Computer Science & Robotics
Date: October 2026

Abstract:
This work presents a novel transformer-lidar hybrid model capable of sub-5ms trajectory re-planning.
Proprietary algorithms, neural architecture weights, and experimental validation logs are strictly confidential.
Any unauthorized copying, distribution, or external disclosure violates University Code of Conduct Sec. 4.12.
"""
    with open(os.path.join(proj_dir, "project_final_report.docx"), "w", encoding="utf-8") as f:
        f.write(docx_text)

    # 2. NTFS MFT Timeline / File System Logs
    mft_file = os.path.join(base_dir, "filesystem", "mft_timeline.csv")
    mft_records = [
        ["RecordID", "Timestamp_UTC", "Action", "FilePath", "FileSize_Bytes", "UserAccount", "ProcessName", "MACB_Flags", "Notes"],
        ["MFT-10492", "2026-10-04 09:15:00", "FILE_MODIFY", "C:\\Projects\\FinalYear_DroneAI\\drone_nav_core.py", "1420", "amercer", "code.exe", "M...", "Routine development by author"],
        ["MFT-10493", "2026-10-04 10:45:22", "FILE_MODIFY", "C:\\Projects\\FinalYear_DroneAI\\dataset_lidar_final.parquet", "81920000", "amercer", "python.exe", "M.B.", "Test flight dataset export"],
        ["MFT-10494", "2026-10-04 16:30:10", "FILE_MODIFY", "C:\\Projects\\FinalYear_DroneAI\\project_final_report.docx", "452000", "amercer", "winword.exe", "M...", "Draft thesis updated"],
        ["MFT-10500", "2026-10-04 18:05:00", "SESSION_LOCK", "C:\\Windows\\System32\\LogonUI.exe", "0", "amercer", "winlogon.exe", "....", "Workstation locked as Alex Mercer left for dinner"],
        ["MFT-10512", "2026-10-04 18:17:45", "FILE_ACCESS", "C:\\Projects\\FinalYear_DroneAI\\drone_nav_core.py", "1420", "dvance", "explorer.exe", ".A..", "Unauthorized directory traversal into Alex project"],
        ["MFT-10513", "2026-10-04 18:17:50", "FILE_ACCESS", "C:\\Projects\\FinalYear_DroneAI\\neural_weights_v4.bin", "52428800", "dvance", "explorer.exe", ".A..", "Accessed proprietary weights"],
        ["MFT-10514", "2026-10-04 18:17:55", "FILE_ACCESS", "C:\\Projects\\FinalYear_DroneAI\\dataset_lidar_final.parquet", "81920000", "dvance", "explorer.exe", ".A..", "Accessed lidar test datasets"],
        ["MFT-10515", "2026-10-04 18:18:02", "FILE_ACCESS", "C:\\Projects\\FinalYear_DroneAI\\project_final_report.docx", "452000", "dvance", "explorer.exe", ".A..", "Accessed dissertation document"],
        ["MFT-10520", "2026-10-04 18:22:10", "FILE_CREATE", "C:\\Users\\Public\\project_backup_v2.zip", "142840112", "dvance", "7z.exe", "MACB", "Staging archive created containing all project files"],
        ["MFT-10535", "2026-10-04 18:29:12", "FILE_CREATE", "E:\\Stolen_Dump\\project_backup_v2.zip", "142840112", "dvance", "explorer.exe", "M.C.", "Copy attempted to Removable USB Drive (SanDisk)"],
        ["MFT-10548", "2026-10-04 18:31:20", "FILE_ACCESS", "C:\\Users\\Public\\project_backup_v2.zip", "142840112", "dvance", "chrome.exe", ".A..", "Staging archive selected in browser file upload picker"],
        ["MFT-10560", "2026-10-04 18:41:50", "FILE_DELETE", "C:\\Users\\Public\\project_backup_v2.zip", "0", "dvance", "cmd.exe", "....", "Anti-forensics cleanup: Staging zip deleted via del command"]
    ]
    with open(mft_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(mft_records)

    # 3. Deleted/Staging Recovery Artifact
    del_dir = os.path.join(base_dir, "filesystem", "deleted_staging")
    deleted_meta = {
        "recovered_artifact_id": "CARVED-ZIP-001",
        "original_path": "C:\\Users\\Public\\project_backup_v2.zip",
        "carved_from_cluster": 4892140,
        "signature": "PK\\x03\\x04 (ZIP Archive)",
        "file_size_bytes": 142840112,
        "creation_time_utc": "2026-10-04 18:22:10",
        "deletion_time_utc": "2026-10-04 18:41:50",
        "archive_manifest": [
            {"filename": "drone_nav_core.py", "uncompressed_size": 1420, "crc32": "7F82A1B0"},
            {"filename": "neural_weights_v4.bin", "uncompressed_size": 52428800, "crc32": "C319E492"},
            {"filename": "dataset_lidar_final.parquet", "uncompressed_size": 81920000, "crc32": "89DF021A"},
            {"filename": "project_final_report.docx", "uncompressed_size": 452000, "crc32": "4B1883F1"}
        ],
        "deleted_by_process": "cmd.exe /c del C:\\Users\\Public\\project_backup_v2.zip",
        "recovery_status": "FULL_METADATA_AND_HEADER_RECOVERED"
    }
    with open(os.path.join(del_dir, "project_backup_v2.zip.deleted.meta"), "w", encoding="utf-8") as f:
        json.dump(deleted_meta, f, indent=2)

    # 4. Auth & Security Event Logs
    auth_dir = os.path.join(base_dir, "auth_logs")
    sec_events = [
        {
            "EventID": 4624,
            "Timestamp_UTC": "2026-10-04 08:30:15",
            "EventType": "Logon",
            "LogonType": 2,
            "LogonTypeDescription": "Interactive (Console)",
            "TargetUserName": "amercer",
            "TargetDomainName": "LAB-DOMAIN",
            "WorkstationName": "LAB-WS-07",
            "IpAddress": "127.0.0.1",
            "IpPort": "0",
            "Status": "Success",
            "Notes": "Normal morning logon by legitimate student Alex Mercer"
        },
        {
            "EventID": 4800,
            "Timestamp_UTC": "2026-10-04 18:05:00",
            "EventType": "Workstation Locked",
            "TargetUserName": "amercer",
            "WorkstationName": "LAB-WS-07",
            "Notes": "Alex Mercer locks workstation screen before leaving for dinner"
        },
        {
            "EventID": 4624,
            "Timestamp_UTC": "2026-10-04 18:14:22",
            "EventType": "Logon",
            "LogonType": 10,
            "LogonTypeDescription": "RemoteInteractive (RDP)",
            "TargetUserName": "dvance",
            "TargetDomainName": "LAB-DOMAIN",
            "WorkstationName": "DEV-LAPTOP-14",
            "IpAddress": "192.168.1.78",
            "IpPort": "49822",
            "Status": "Success",
            "Notes": "UNAUTHORIZED REMOTE DESKTOP SESSION established from David Vance laptop"
        },
        {
            "EventID": 4688,
            "Timestamp_UTC": "2026-10-04 18:22:08",
            "EventType": "Process Creation",
            "SubjectUserName": "dvance",
            "NewProcessName": "C:\\Program Files\\7-Zip\\7z.exe",
            "CommandLine": '7z.exe a -tzip C:\\Users\\Public\\project_backup_v2.zip C:\\Projects\\FinalYear_DroneAI\\*',
            "ParentProcessName": "C:\\Windows\\System32\\cmd.exe",
            "Notes": "Compression tool used to bundle all project files into staging area"
        },
        {
            "EventID": 7045,
            "Timestamp_UTC": "2026-10-04 18:28:30",
            "EventType": "Service Installed / Driver Load",
            "ServiceName": "USBSTOR",
            "ImagePath": "C:\\Windows\\System32\\drivers\\USBSTOR.SYS",
            "ServiceType": "Kernel Driver",
            "Notes": "USB Storage driver engaged upon external drive connection"
        },
        {
            "EventID": 4688,
            "Timestamp_UTC": "2026-10-04 18:31:10",
            "EventType": "Process Creation",
            "SubjectUserName": "dvance",
            "NewProcessName": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            "CommandLine": '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --incognito https://dropfile.to',
            "ParentProcessName": "C:\\Windows\\explorer.exe",
            "Notes": "Browser launched in incognito mode targeting file upload service"
        },
        {
            "EventID": 4688,
            "Timestamp_UTC": "2026-10-04 18:41:48",
            "EventType": "Process Creation",
            "SubjectUserName": "dvance",
            "NewProcessName": "C:\\Windows\\System32\\cmd.exe",
            "CommandLine": 'cmd.exe /c del /f /q C:\\Users\\Public\\project_backup_v2.zip',
            "ParentProcessName": "C:\\Windows\\explorer.exe",
            "Notes": "Command executed to delete staging zip file from disk"
        },
        {
            "EventID": 4634,
            "Timestamp_UTC": "2026-10-04 18:42:10",
            "EventType": "Logoff",
            "LogonType": 10,
            "TargetUserName": "dvance",
            "TargetDomainName": "LAB-DOMAIN",
            "WorkstationName": "DEV-LAPTOP-14",
            "IpAddress": "192.168.1.78",
            "Notes": "David Vance terminates RDP session after exfiltration"
        }
    ]
    with open(os.path.join(auth_dir, "Security_EventLogs.json"), "w", encoding="utf-8") as f:
        json.dump(sec_events, f, indent=2)

    sys_reg = {
        "RegistryHive": "SYSTEM / NTUSER.DAT (dvance)",
        "USBSTOR_Artifacts": [
            {
                "DeviceClass": "Disk",
                "Vendor": "SanDisk",
                "Product": "Ultra USB 3.0",
                "SerialNumber": "4C530001290818115243",
                "VolumeGuid": "{d3f4a10e-8a12-4c28-98e3-0941bc4a72e9}",
                "AssignedDriveLetter": "E:",
                "FirstInstallDate_UTC": "2026-10-04 18:28:30",
                "LastArrivalDate_UTC": "2026-10-04 18:28:30",
                "LastRemovalDate_UTC": "2026-10-04 18:40:15",
                "RegisteredOwner": "David Vance (Registered in Lab Device Asset Database)"
            }
        ],
        "UserAssist_MRU": [
            {"Executable": "7z.exe", "RunCount": 1, "LastExecution_UTC": "2026-10-04 18:22:08"},
            {"Executable": "chrome.exe", "RunCount": 4, "LastExecution_UTC": "2026-10-04 18:31:10"},
            {"Executable": "cmd.exe", "RunCount": 3, "LastExecution_UTC": "2026-10-04 18:41:48"}
        ],
        "Shellbags_FolderAccess": [
            {"FolderPath": "C:\\Projects\\FinalYear_DroneAI", "LastAccess_UTC": "2026-10-04 18:17:45", "AccessingUser": "dvance"},
            {"FolderPath": "C:\\Users\\Public", "LastAccess_UTC": "2026-10-04 18:22:15", "AccessingUser": "dvance"},
            {"FolderPath": "E:\\Stolen_Dump", "LastAccess_UTC": "2026-10-04 18:29:10", "AccessingUser": "dvance"}
        ]
    }
    with open(os.path.join(auth_dir, "system_registry.json"), "w", encoding="utf-8") as f:
        json.dump(sys_reg, f, indent=2)

    # 5. Browser History (Real SQLite DB)
    browser_dir = os.path.join(base_dir, "browser")
    sqlite_path = os.path.join(browser_dir, "chrome_history.sqlite")
    if os.path.exists(sqlite_path):
        os.remove(sqlite_path)

    conn = sqlite3.connect(sqlite_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE urls (
            id INTEGER PRIMARY KEY,
            url TEXT NOT NULL,
            title TEXT,
            visit_count INTEGER DEFAULT 1,
            typed_count INTEGER DEFAULT 0,
            last_visit_time INTEGER NOT NULL,
            hidden INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE visits (
            id INTEGER PRIMARY KEY,
            url INTEGER NOT NULL,
            visit_time INTEGER NOT NULL,
            from_visit INTEGER,
            transition INTEGER,
            FOREIGN KEY(url) REFERENCES urls(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE downloads (
            id INTEGER PRIMARY KEY,
            guid TEXT,
            current_path TEXT,
            target_path TEXT,
            start_time INTEGER,
            received_bytes INTEGER,
            total_bytes INTEGER,
            state INTEGER,
            danger_type INTEGER,
            interrupt_reason INTEGER,
            raw_url TEXT,
            referrer TEXT,
            mime_type TEXT
        )
    """)

    # Chrome timestamp: microseconds since Jan 1, 1601 UTC
    # 2026-10-04 18:31:15 UTC -> WebKit timestamp
    urls_data = [
        (1, "https://www.google.com/search?q=anonymous+fast+file+sharing+no+registration", "anonymous fast file sharing - Google Search", 1, 1, 13435113075000000, 0),
        (2, "https://dropfile.to/", "DropFile.to - Free Anonymous Large File Transfer", 2, 1, 13435113090000000, 0),
        (3, "https://dropfile.to/api/upload", "DropFile API Endpoint", 1, 0, 13435113340000000, 0),
        (4, "https://dropfile.to/d/9x8K2L1q", "DropFile.to - Download project_backup_v2.zip", 1, 0, 13435113350000000, 0),
        (5, "https://tempmail.org/", "Temp Mail - Disposable Temporary Email", 2, 1, 13435113420000000, 0),
        (6, "https://mail.proton.me/login", "Proton Mail: Secure & Encrypted Email", 1, 1, 13435113480000000, 0)
    ]
    cursor.executemany("INSERT INTO urls VALUES (?,?,?,?,?,?,?)", urls_data)

    visits_data = [
        (1, 1, 13435113075000000, 0, 805306368),
        (2, 2, 13435113090000000, 1, 805306368),
        (3, 3, 13435113340000000, 2, 805306368),
        (4, 4, 13435113350000000, 3, 805306368),
        (5, 5, 13435113420000000, 0, 805306368),
        (6, 6, 13435113480000000, 0, 805306368)
    ]
    cursor.executemany("INSERT INTO visits VALUES (?,?,?,?,?)", visits_data)
    conn.commit()
    conn.close()

    cache_meta = {
        "Browser": "Google Chrome 130.0.6723.70 (x64)",
        "Profile": "Default (Incognito Session Active)",
        "ActiveSessionUser": "dvance",
        "FormUploadArtefacts": [
            {
                "Timestamp_UTC": "2026-10-04 18:35:40",
                "Action": "HTTP_MULTIPART_POST_UPLOAD",
                "Destination_URL": "https://dropfile.to/api/upload",
                "Destination_IP": "185.220.101.42",
                "Source_File_Path": "C:\\Users\\Public\\project_backup_v2.zip",
                "File_Size_Bytes": 142840112,
                "Content_Type": "application/zip",
                "Server_Response_JSON": {
                    "status": "success",
                    "file_id": "9x8K2L1q",
                    "file_name": "project_backup_v2.zip",
                    "download_url": "https://dropfile.to/d/9x8K2L1q",
                    "pass_code": "droneAI_v4_secret",
                    "expires_in": "86400",
                    "uploaded_from_ip": "192.168.1.45"
                }
            }
        ]
    }
    with open(os.path.join(browser_dir, "chrome_cache_metadata.json"), "w", encoding="utf-8") as f:
        json.dump(cache_meta, f, indent=2)

    # 6. Email Evidence
    email_dir = os.path.join(base_dir, "email")
    exfil_eml = """From: "David Vance" <david.vance99@protonmail.com>
To: "Dr. Jonathan Stern" <j.stern@competitor-lab.org>
Cc: "David Vance (Student)" <dvance@university.edu>
Subject: Final Drone AI Codebase & Trained Model Weights (Alex's Project)
Date: Sun, 4 Oct 2026 18:38:05 +0000
Message-ID: <CABp=8gP7xQ8L1m+u99k2819_exfil@mail.proton.me>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
X-Originating-IP: [192.168.1.78]
X-Mailer: ProtonMail Web Client v5.0.32
Authentication-Results: mail.competitor-lab.org; dkim=pass header.i=@protonmail.com

Dear Dr. Stern,

Following our discussion regarding the funded research fellowship in your autonomous robotics lab, I have secured the full proprietary repository for the real-time Transformer LiDAR obstacle avoidance system from Alex Mercer's workstation here at the University.

Because the entire repository (source code, trained model weights, lidar point cloud evaluation datasets, and full dissertation draft) exceeds email attachment limits (~142.8 MB), I have staged and uploaded the encrypted archive to an anonymous secure drop:

Download Link: https://dropfile.to/d/9x8K2L1q
Access Passcode: droneAI_v4_secret
MD5 Checksum: e4d909c290d0fb1ca068ffaddf22cbd0

Contents in archive:
1. drone_nav_core.py (Transformer-LiDAR hybrid navigation algorithm)
2. neural_weights_v4.bin (Trained weights from 500+ simulated GPU flight hours)
3. dataset_lidar_final.parquet (Raw proprietary benchmark point cloud data)
4. project_final_report.docx (Complete technical writeup and patent disclosures)

Please confirm once you have downloaded the files so I can purge the upload link. I look forward to finalizing my fellowship offer letter next week.

Best regards,
David Vance
Department of Computer Science & Robotics
Student ID: CS-2026-9012
"""
    with open(os.path.join(email_dir, "exfil_notification.eml"), "w", encoding="utf-8") as f:
        f.write(exfil_eml)

    phish_eml = """From: "David Vance" <dvance@university.edu>
To: "Alex Mercer" <amercer@university.edu>
Subject: Quick question about your LiDAR training scripts
Date: Fri, 2 Oct 2026 14:12:00 +0000
Message-ID: <UNIV-MSG-20261002-8812@university.edu>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8

Hey Alex,

Great presentation at the departmental seminar yesterday! Are you keeping all your final training weights and dataset parquet files on your local workstation drive C:\\Projects\\FinalYear_DroneAI or are they synced to the departmental network share?

Wanted to benchmark my path-planning script against your latest weights if possible.

Thanks,
David
"""
    with open(os.path.join(email_dir, "internal_phishing.eml"), "w", encoding="utf-8") as f:
        f.write(phish_eml)

    # 7. Network Information / Logs
    net_dir = os.path.join(base_dir, "network")
    netflow_records = [
        ["FlowID", "Timestamp_UTC", "SourceIP", "SourcePort", "DestinationIP", "DestinationPort", "Protocol", "BytesTransferred", "Packets", "Duration_Sec", "Flags", "ApplicationProtocol", "Notes"],
        ["FLOW-8810", "2026-10-04 18:14:20", "192.168.1.78", "49822", "192.168.1.45", "3389", "TCP", "4210500", "3820", "1720", "ESTABLISHED", "RDP", "Inbound RDP from David Vance laptop to Victim Workstation"],
        ["FLOW-8824", "2026-10-04 18:31:12", "192.168.1.45", "51204", "8.8.8.8", "53", "UDP", "142", "2", "0.05", "COMPLETED", "DNS", "DNS Query for dropfile.to -> 185.220.101.42"],
        ["FLOW-8825", "2026-10-04 18:31:14", "192.168.1.45", "51206", "185.220.101.42", "443", "TCP", "48200", "64", "4.2", "ESTABLISHED", "TLS/HTTPS", "Initial HTTPS connection to dropfile.to landing page"],
        ["FLOW-8830", "2026-10-04 18:35:35", "192.168.1.45", "51240", "185.220.101.42", "443", "TCP", "143120400", "98420", "42.5", "ESTABLISHED", "TLS/HTTPS", "MASSIVE EXFILTRATION: Upload of 142.8 MB zip archive to dropfile.to"],
        ["FLOW-8835", "2026-10-04 18:38:00", "192.168.1.78", "52100", "185.70.40.185", "443", "TCP", "185400", "142", "6.1", "ESTABLISHED", "TLS/HTTPS", "ProtonMail webmail connection to send exfiltration email"]
    ]
    with open(os.path.join(net_dir, "netflow_connections.csv"), "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(netflow_records)

    pcap_summary = {
        "CaptureFile": "lab_gateway_span_20261004.pcap",
        "CaptureTime_UTC": "2026-10-04 18:00:00 to 19:00:00",
        "MonitoredSubnet": "192.168.1.0/24",
        "DNS_Queries": [
            {"Timestamp_UTC": "2026-10-04 18:31:12", "ClientIP": "192.168.1.45", "Query": "dropfile.to", "AnswerIP": "185.220.101.42", "TTL": 300},
            {"Timestamp_UTC": "2026-10-04 18:34:10", "ClientIP": "192.168.1.45", "Query": "tempmail.org", "AnswerIP": "104.21.34.12", "TTL": 300},
            {"Timestamp_UTC": "2026-10-04 18:37:50", "ClientIP": "192.168.1.78", "Query": "mail.proton.me", "AnswerIP": "185.70.40.185", "TTL": 300}
        ],
        "TLS_SNI_Sessions": [
            {"Timestamp_UTC": "2026-10-04 18:14:20", "SrcIP": "192.168.1.78", "DstIP": "192.168.1.45", "Port": 3389, "Protocol": "RDP", "Service": "Terminal Services"},
            {"Timestamp_UTC": "2026-10-04 18:35:35", "SrcIP": "192.168.1.45", "DstIP": "185.220.101.42", "Port": 443, "SNI": "dropfile.to", "BytesOut": 143120400, "Method": "POST /api/upload"},
            {"Timestamp_UTC": "2026-10-04 18:38:00", "SrcIP": "192.168.1.78", "DstIP": "185.70.40.185", "Port": 443, "SNI": "mail.proton.me", "BytesOut": 185400, "Method": "POST /api/messages"}
        ]
    }
    with open(os.path.join(net_dir, "pcap_dns_http_summary.json"), "w", encoding="utf-8") as f:
        json.dump(pcap_summary, f, indent=2)

    print("[SUCCESS] Complete simulated digital forensics evidence dataset generated.")

if __name__ == "__main__":
    create_evidence()
