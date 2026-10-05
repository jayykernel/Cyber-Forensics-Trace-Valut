def build_attack_chain(timeline):
    """
    Correlate cross-artefact evidence into a structured sequential multi-hop attack chain.
    """
    chain_stages = [
        {
            "stage": 1,
            "title": "Unauthorized Access & Lateral Ingress",
            "source_type": "Authentication / Network",
            "details": "Remote Desktop (RDP) connection established to victim workstation LAB-WS-07 (192.168.1.45:3389) from DEV-LAPTOP-14 (192.168.1.78) using account 'dvance'.",
            "evidence_refs": ["EventID: 4624 (Logon Type 10)", "FlowID: FLOW-8810"],
            "timestamp": "2026-10-04 18:14:20"
        },
        {
            "stage": 2,
            "title": "Directory Traversal & Confidential File Access",
            "source_type": "NTFS MFT / Shellbags",
            "details": "User 'dvance' traversed Alex Mercer's confidential folder 'C:\\Projects\\FinalYear_DroneAI\\' and accessed core algorithms, model weights, lidar datasets, and final dissertation.",
            "evidence_refs": ["MFT-10512", "MFT-10513", "MFT-10514", "MFT-10515", "NTUSER.DAT\\Shellbags"],
            "timestamp": "2026-10-04 18:17:45"
        },
        {
            "stage": 3,
            "title": "Data Staging & Compression",
            "source_type": "Process Execution / File System",
            "details": "Creation of single staging archive 'C:\\Users\\Public\\project_backup_v2.zip' (142.8 MB) using 7z.exe containing all four critical project files.",
            "evidence_refs": ["EventID: 4688 (7z.exe)", "MFT-10520", "CARVED-ZIP-001"],
            "timestamp": "2026-10-04 18:22:10"
        },
        {
            "stage": 4,
            "title": "Physical / Secondary Exfiltration Attempt",
            "source_type": "Registry (USBSTOR)",
            "details": "Insertion of SanDisk Ultra USB 3.0 (Serial: 4C530001290818115243) mounted as E:\\, followed by copying staging archive to E:\\Stolen_Dump.",
            "evidence_refs": ["HKLM\\SYSTEM\\...\\USBSTOR", "MFT-10535"],
            "timestamp": "2026-10-04 18:28:30"
        },
        {
            "stage": 5,
            "title": "Network Cloud Exfiltration",
            "source_type": "Browser / Netflow / PCAP",
            "details": "Chrome launched in incognito mode to dropfile.to. Staging archive uploaded via HTTP POST to 185.220.101.42 (143,120,400 bytes). Received public download link https://dropfile.to/d/9x8K2L1q.",
            "evidence_refs": ["chrome_cache_metadata.json", "FLOW-8830", "PCAP SNI: dropfile.to"],
            "timestamp": "2026-10-04 18:35:40"
        },
        {
            "stage": 6,
            "title": "External Distribution & Monetization",
            "source_type": "Email Artefacts / Network Flow",
            "details": "David Vance sent an email from david.vance99@protonmail.com to competitor lab (j.stern@competitor-lab.org) containing the dropfile.to link and encryption password.",
            "evidence_refs": ["exfil_notification.eml", "FLOW-8835", "PCAP SNI: mail.proton.me"],
            "timestamp": "2026-10-04 18:38:05"
        },
        {
            "stage": 7,
            "title": "Anti-Forensics & Log Scrubbing",
            "source_type": "Process Execution / MFT",
            "details": "Execution of 'cmd.exe /c del' to permanently delete staging archive from C:\\Users\\Public\\ and termination of RDP session.",
            "evidence_refs": ["EventID: 4688 (cmd.exe del)", "MFT-10560", "EventID: 4634 (Logoff)"],
            "timestamp": "2026-10-04 18:41:50"
        }
    ]
    return chain_stages
