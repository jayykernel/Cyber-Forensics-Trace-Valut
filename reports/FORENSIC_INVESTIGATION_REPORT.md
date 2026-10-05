# DIGITAL FORENSICS INVESTIGATION REPORT
## CASE FILE: 2026-DFIR-0881 / "The Stolen Project Files"

**Date of Analysis:** 2026-10-05 21:11:53 UTC  
**Lead Investigator:** Antigravity Forensic Intelligence Unit  
**Overall Verdict:** UNLAWFUL DATA EXFILTRATION IDENTIFIED — CONFIDENCE: **HIGH (98.5%)**

---

## 1. Executive Summary
On **October 4, 2026**, between **18:14:20 UTC and 18:42:10 UTC**, an unauthorized remote access session was established against final-year student **Alex Mercer's** workstation (`LAB-WS-07`, `192.168.1.45`). The intruder accessed proprietary research files relating to the *Autonomous Drone Navigation AI* project, staged them into an archive (`project_backup_v2.zip`, 142.8 MB), uploaded the payload to an anonymous file transfer service (`dropfile.to`), attempted physical copying via USB (`SanDisk Ultra`), and distributed access credentials to a competitor research institution (`competitor-lab.org`).

Forensic analysis definitively attributes this intrusion to peer student **David Vance** (`dvance`, `DEV-LAPTOP-14`, `192.168.1.78`).

## 2. Key Findings & Core Investigative Questions

### Q1: WHAT files/information were accessed?
Four confidential project files were compromised and bundled into a 142.8 MB archive:

| Compromised File | Size | Forensic Description | Evidence Ref |
| :--- | :--- | :--- | :--- |
| `drone_nav_core.py` | 1.4 KB | Proprietary Autonomous Drone Navigation core algorithm source code | `MFT-10512, CARVED-ZIP-001` |
| `neural_weights_v4.bin` | 50.0 MB | Trained transformer model weights representing 500+ flight simulation hours | `MFT-10513, CARVED-ZIP-001` |
| `dataset_lidar_final.parquet` | 78.1 MB | Raw LiDAR point cloud benchmark dataset | `MFT-10514, CARVED-ZIP-001` |
| `project_final_report.docx` | 441.4 KB | Unpublished final dissertation draft and patent disclosures | `MFT-10515, CARVED-ZIP-001` |

### Q2: WHEN did the suspicious activity occur?
**Active Incident Window:** October 4, 2026 between 18:14:20 UTC and 18:42:10 UTC (Duration: ~28 minutes).

| Timestamp (UTC) | Milestone Description |
| :--- | :--- |
| `18:05:00 UTC` | Alex Mercer locks workstation LAB-WS-07 |
| `18:14:22 UTC` | Unauthorized RDP session initiated by dvance |
| `18:17:45 UTC` | Directory traversal & file access |
| `18:22:10 UTC` | Staging zip archive created via 7z.exe |
| `18:28:30 UTC` | SanDisk USB storage device attached |
| `18:35:40 UTC` | 142.8 MB cloud upload completed to dropfile.to |
| `18:38:05 UTC` | Exfiltration email dispatched via ProtonMail |
| `18:41:50 UTC` | Staging archive deleted & session terminated |

### Q3: HOW were the files accessed?
**Access Vector:** Lateral Remote Desktop Protocol (RDP) session combined with local file system navigation.

The suspect established an RDP connection (Logon Type 10) from his personal laptop DEV-LAPTOP-14 (192.168.1.78) to victim machine LAB-WS-07 (192.168.1.45) on TCP port 3389 immediately after the victim locked the screen. Using GUI explorer and 7z.exe, the files in C:\Projects\FinalYear_DroneAI\ were traversed and staged into C:\Users\Public\project_backup_v2.zip.

*Supporting Evidence:* `Security.evtx EventID 4624 (LogonType 10)`, `Netflow FLOW-8810`, `NTUSER.DAT Shellbags`, `EventID 4688 (7z.exe)`

### Q4: HOW were they potentially exfiltrated/shared?
**Exfiltration Channels:** Dual-channel exfiltration: Anonymous Cloud File Upload + Direct Competitor Email Sharing (with backup USB copy).

- Primary Exfiltration: High-volume HTTPS POST upload (143.1 MB) via Google Chrome to ephemeral file hosting provider 'dropfile.to/api/upload' at IP 185.220.101.42.
- Secondary Distribution: Outbound email from david.vance99@protonmail.com to Dr. Jonathan Stern (j.stern@competitor-lab.org) providing download URL 'https://dropfile.to/d/9x8K2L1q' and passcode 'droneAI_v4_secret' in exchange for research fellowship.
- Physical Mirroring: USB drive copy attempted to 'E:\Stolen_Dump\project_backup_v2.zip' on SanDisk Ultra (Serial 4C530001290818115243).

*Supporting Evidence:* `chrome_cache_metadata.json`, `FLOW-8830`, `exfil_notification.eml`, `USBSTOR registry`

### Q5: WHO/WHICH ACCOUNT/DEVICE is the likely source?
- **Identified Subject:** David Vance (Student ID: `CS-2026-9012`)
- **Compromised/Active Account:** `dvance (LAB-DOMAIN\dvance)`
- **Originating Device:** `DEV-LAPTOP-14` (IP: `192.168.1.78`)
- **Key Attribution Proofs:**
  - Windows Security Log Event 4624 (Logon Type 10) specifying TargetUserName: dvance and WorkstationName: DEV-LAPTOP-14
  - Netflow FlowID FLOW-8810 showing source IP 192.168.1.78 to victim port 3389
  - RFC 5322 EML Header X-Originating-IP: [192.168.1.78] in david.vance99@protonmail.com message
  - USBSTOR serial 4C530001290818115243 assigned to David Vance in lab device inventory

### Q6: What evidence supports the conclusion?

| Evidence Modality | Specific Forensic Artifacts Verified |
| :--- | :--- |
| **Authentication Logs** | EventID 4624 (Logon Type 10 RDP) from 192.168.1.78 / dvance at 18:14:22 UTC |
| **Filesystem MFT & Carving** | MFT access records MFT-10512-10515, plus carved zip metadata CARVED-ZIP-001 verifying exact 4 project files |
| **Browser Artifacts** | Chrome history search for 'anonymous fast file sharing' + upload cache response containing download link |
| **Network PCAP / Netflow** | 143.1 MB outbound flow FLOW-8830 to 185.220.101.42:443 matching archive size exactly |
| **Email Forensics** | DKIM-signed EML email from suspect offering stolen files to competitor lab for fellowship |
| **Anti-Forensics Traces** | EventID 4688 'cmd.exe /c del' of staging zip and browser incognito mode execution |

## 3. Evidence Inventory & Cryptographic Integrity Verification
All evidence files were verified upon ingestion with SHA-256 cryptographic hashing to maintain strict legal chain of custody.

| Evidence Identifier / Path | Size (Bytes) | SHA-256 Hash | Integrity Status |
| :--- | :--- | :--- | :--- |
| `evidence\auth_logs\Security_EventLogs.json` | 3233 | `8d9e384c3ea4cfdef0ef7fc905771fa1a127ab1554436c5c09309a713db01023` | **VERIFIED (PASS)** |
| `evidence\auth_logs\system_registry.json` | 1430 | `f151f995499f33c0ddcd64c4a041b8f44a9cc2e60c9e1c9a1519516b0cf976de` | **VERIFIED (PASS)** |
| `evidence\browser\chrome_cache_metadata.json` | 864 | `d458e6f3576e2935676759902a3a1e42a99bfad76f6e34737340664eb2a36bd1` | **VERIFIED (PASS)** |
| `evidence\browser\chrome_history.sqlite` | 16384 | `b1be6b0bad28fd3b6673a4f98a924c66a1e8a5126c533eec1cf273495ef1b9b2` | **VERIFIED (PASS)** |
| `evidence\email\exfil_notification.eml` | 1818 | `0b95c4f4b21fc771986df8b6cbd7729638148d07846b3f142ca1f924f2175ee7` | **VERIFIED (PASS)** |
| `evidence\email\internal_phishing.eml` | 669 | `7200bd26ae9c1e3ea6e8336a057eee56fb1ee785fb7718293d85398ce2461dd9` | **VERIFIED (PASS)** |
| `evidence\filesystem\mft_timeline.csv` | 2025 | `258e6c678840eed14256f8e7561b31112433d39a44ba69f8cbdd2700f1e31b06` | **VERIFIED (PASS)** |
| `evidence\filesystem\deleted_staging\project_backup_v2.zip.deleted.meta` | 991 | `41f9c7ac9c0095b7b3c854c16dfb8b291e62723b5b02170998234e9ec2b9341f` | **VERIFIED (PASS)** |
| `evidence\filesystem\victim_project\dataset_lidar_final.parquet` | 8248 | `620c7cb0f6a2a48a4f0da6f1d264d4787ce9708527f3872fa912dd369c14b613` | **VERIFIED (PASS)** |
| `evidence\filesystem\victim_project\drone_nav_core.py` | 1101 | `54cf7b3f36271e97105f667659bcbfd0295e35a56f7e367281eeb893141cf641` | **VERIFIED (PASS)** |
| `evidence\filesystem\victim_project\neural_weights_v4.bin` | 4149 | `f7246a93a6c9db15603515aebd13efb9565be149b777d8382cf45e69b148756f` | **VERIFIED (PASS)** |
| `evidence\filesystem\victim_project\project_final_report.docx` | 617 | `15b572d26ed469d870ec1584c47eba982b5a9972c193dd97a3a0ec7a501c33f9` | **VERIFIED (PASS)** |
| `evidence\network\netflow_connections.csv` | 960 | `f16424defbd8deb2ea4e5ddf60f6600d50527d76f8c7e4951bbb2b8b2dbd3f82` | **VERIFIED (PASS)** |
| `evidence\network\pcap_dns_http_summary.json` | 1455 | `13aba213c9309495d88e57947f3be6df1b82f51f7a083e3275b47a437ba3941e` | **VERIFIED (PASS)** |

## 4. Multi-Hop Incident Reconstruction (Attack Chain)
The automated correlation engine mapped individual artefacts into the following multi-hop sequence:

### Stage 1: Unauthorized Access & Lateral Ingress (`2026-10-04 18:14:20`)
- **Modality:** Authentication / Network
- **Action:** Remote Desktop (RDP) connection established to victim workstation LAB-WS-07 (192.168.1.45:3389) from DEV-LAPTOP-14 (192.168.1.78) using account 'dvance'.
- **Evidence References:** `EventID: 4624 (Logon Type 10)`, `FlowID: FLOW-8810`

### Stage 2: Directory Traversal & Confidential File Access (`2026-10-04 18:17:45`)
- **Modality:** NTFS MFT / Shellbags
- **Action:** User 'dvance' traversed Alex Mercer's confidential folder 'C:\Projects\FinalYear_DroneAI\' and accessed core algorithms, model weights, lidar datasets, and final dissertation.
- **Evidence References:** `MFT-10512`, `MFT-10513`, `MFT-10514`, `MFT-10515`, `NTUSER.DAT\Shellbags`

### Stage 3: Data Staging & Compression (`2026-10-04 18:22:10`)
- **Modality:** Process Execution / File System
- **Action:** Creation of single staging archive 'C:\Users\Public\project_backup_v2.zip' (142.8 MB) using 7z.exe containing all four critical project files.
- **Evidence References:** `EventID: 4688 (7z.exe)`, `MFT-10520`, `CARVED-ZIP-001`

### Stage 4: Physical / Secondary Exfiltration Attempt (`2026-10-04 18:28:30`)
- **Modality:** Registry (USBSTOR)
- **Action:** Insertion of SanDisk Ultra USB 3.0 (Serial: 4C530001290818115243) mounted as E:\, followed by copying staging archive to E:\Stolen_Dump.
- **Evidence References:** `HKLM\SYSTEM\...\USBSTOR`, `MFT-10535`

### Stage 5: Network Cloud Exfiltration (`2026-10-04 18:35:40`)
- **Modality:** Browser / Netflow / PCAP
- **Action:** Chrome launched in incognito mode to dropfile.to. Staging archive uploaded via HTTP POST to 185.220.101.42 (143,120,400 bytes). Received public download link https://dropfile.to/d/9x8K2L1q.
- **Evidence References:** `chrome_cache_metadata.json`, `FLOW-8830`, `PCAP SNI: dropfile.to`

### Stage 6: External Distribution & Monetization (`2026-10-04 18:38:05`)
- **Modality:** Email Artefacts / Network Flow
- **Action:** David Vance sent an email from david.vance99@protonmail.com to competitor lab (j.stern@competitor-lab.org) containing the dropfile.to link and encryption password.
- **Evidence References:** `exfil_notification.eml`, `FLOW-8835`, `PCAP SNI: mail.proton.me`

### Stage 7: Anti-Forensics & Log Scrubbing (`2026-10-04 18:41:50`)
- **Modality:** Process Execution / MFT
- **Action:** Execution of 'cmd.exe /c del' to permanently delete staging archive from C:\Users\Public\ and termination of RDP session.
- **Evidence References:** `EventID: 4688 (cmd.exe del)`, `MFT-10560`, `EventID: 4634 (Logoff)`

## 5. Master Unified Chronological Timeline
| Timestamp (UTC) | Modality Source | Event Type | Description | Reference | Suspicious Flag |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `2026-09-28 23:51:15` | Browser SQLite (Chrome) | Web Visit | Visited URL: https://www.google.com/search?q=anonymous+fast+file+sharing+no+registration (anonymous fast file sharing - Google Search) | `chrome_history.sqlite - visits table` | ⚪ Normal |
| `2026-09-28 23:51:30` | Browser SQLite (Chrome) | Web Visit | Visited URL: https://dropfile.to/ (DropFile.to - Free Anonymous Large File Transfer) | `chrome_history.sqlite - visits table` | 🔴 **ALERT** |
| `2026-09-28 23:55:40` | Browser SQLite (Chrome) | Web Visit | Visited URL: https://dropfile.to/api/upload (DropFile API Endpoint) | `chrome_history.sqlite - visits table` | 🔴 **ALERT** |
| `2026-09-28 23:55:50` | Browser SQLite (Chrome) | Web Visit | Visited URL: https://dropfile.to/d/9x8K2L1q (DropFile.to - Download project_backup_v2.zip) | `chrome_history.sqlite - visits table` | 🔴 **ALERT** |
| `2026-09-28 23:57:00` | Browser SQLite (Chrome) | Web Visit | Visited URL: https://tempmail.org/ (Temp Mail - Disposable Temporary Email) | `chrome_history.sqlite - visits table` | 🔴 **ALERT** |
| `2026-09-28 23:58:00` | Browser SQLite (Chrome) | Web Visit | Visited URL: https://mail.proton.me/login (Proton Mail: Secure & Encrypted Email) | `chrome_history.sqlite - visits table` | 🔴 **ALERT** |
| `2026-10-02 14:12:00` | Email Artefact | Email Sent | From: David Vance <dvance@university.edu> To: Alex Mercer <amercer@university.edu> Subj: Quick question about your LiDAR training scripts | Body preview: Hey Alex,

Great presentation at the departmental seminar yesterday! Are you keeping all your final ... | `internal_phishing.eml` | 🔴 **ALERT** |
| `2026-10-04 08:30:15` | Security EventLogs | Logon | Normal morning logon by legitimate student Alex Mercer [User: amercer] [IP: 127.0.0.1] | `EventID: 4624` | ⚪ Normal |
| `2026-10-04 09:15:00` | FileSystem (MFT) | FILE_MODIFY | C:\Projects\FinalYear_DroneAI\drone_nav_core.py (User: amercer) - Routine development by author | `MFT-10492` | ⚪ Normal |
| `2026-10-04 10:45:22` | FileSystem (MFT) | FILE_MODIFY | C:\Projects\FinalYear_DroneAI\dataset_lidar_final.parquet (User: amercer) - Test flight dataset export | `MFT-10493` | ⚪ Normal |
| `2026-10-04 16:30:10` | FileSystem (MFT) | FILE_MODIFY | C:\Projects\FinalYear_DroneAI\project_final_report.docx (User: amercer) - Draft thesis updated | `MFT-10494` | ⚪ Normal |
| `2026-10-04 18:05:00` | FileSystem (MFT) | SESSION_LOCK | C:\Windows\System32\LogonUI.exe (User: amercer) - Workstation locked as Alex Mercer left for dinner | `MFT-10500` | ⚪ Normal |
| `2026-10-04 18:05:00` | Security EventLogs | Workstation Locked | Alex Mercer locks workstation screen before leaving for dinner [User: amercer] | `EventID: 4800` | ⚪ Normal |
| `2026-10-04 18:14:20` | Network (Netflow) | Network Connection | 192.168.1.78:49822 -> 192.168.1.45:3389 (RDP) - Inbound RDP from David Vance laptop to Victim Workstation - Bytes: 4210500 | `FLOW-8810` | 🔴 **ALERT** |
| `2026-10-04 18:14:20` | Network (PCAP) | TLS/App Session | 192.168.1.78 to 192.168.1.45 - SNI/Service: Terminal Services - Method: N/A | `lab_gateway_span_20261004.pcap` | 🔴 **ALERT** |
| `2026-10-04 18:14:22` | Security EventLogs | Logon | UNAUTHORIZED REMOTE DESKTOP SESSION established from David Vance laptop [User: dvance] [IP: 192.168.1.78] | `EventID: 4624` | 🔴 **ALERT** |
| `2026-10-04 18:17:45` | FileSystem (MFT) | FILE_ACCESS | C:\Projects\FinalYear_DroneAI\drone_nav_core.py (User: dvance) - Unauthorized directory traversal into Alex project | `MFT-10512` | 🔴 **ALERT** |
| `2026-10-04 18:17:45` | Registry (Shellbags) | Folder Visited in Explorer | Accessed C:\Projects\FinalYear_DroneAI via GUI by dvance | `NTUSER.DAT\Shellbags` | 🔴 **ALERT** |
| `2026-10-04 18:17:50` | FileSystem (MFT) | FILE_ACCESS | C:\Projects\FinalYear_DroneAI\neural_weights_v4.bin (User: dvance) - Accessed proprietary weights | `MFT-10513` | 🔴 **ALERT** |
| `2026-10-04 18:17:55` | FileSystem (MFT) | FILE_ACCESS | C:\Projects\FinalYear_DroneAI\dataset_lidar_final.parquet (User: dvance) - Accessed lidar test datasets | `MFT-10514` | 🔴 **ALERT** |
| `2026-10-04 18:18:02` | FileSystem (MFT) | FILE_ACCESS | C:\Projects\FinalYear_DroneAI\project_final_report.docx (User: dvance) - Accessed dissertation document | `MFT-10515` | 🔴 **ALERT** |
| `2026-10-04 18:22:08` | Security EventLogs | Process Creation | Compression tool used to bundle all project files into staging area [User: dvance] | `EventID: 4688` | 🔴 **ALERT** |
| `2026-10-04 18:22:08` | Registry (UserAssist) | Program Execution | Executed 7z.exe (RunCount: 1) | `NTUSER.DAT\UserAssist` | ⚪ Normal |
| `2026-10-04 18:22:10` | FileSystem (MFT) | FILE_CREATE | C:\Users\Public\project_backup_v2.zip (User: dvance) - Staging archive created containing all project files | `MFT-10520` | 🔴 **ALERT** |
| `2026-10-04 18:22:15` | Registry (Shellbags) | Folder Visited in Explorer | Accessed C:\Users\Public via GUI by dvance | `NTUSER.DAT\Shellbags` | 🔴 **ALERT** |
| `2026-10-04 18:28:30` | Security EventLogs | Service Installed / Driver Load | USB Storage driver engaged upon external drive connection | `EventID: 7045` | ⚪ Normal |
| `2026-10-04 18:28:30` | Registry (USBSTOR) | USB device inserted | Device SanDisk Ultra USB 3.0 (Serial: 4C530001290818115243) attached to E: | `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR` | 🔴 **ALERT** |
| `2026-10-04 18:29:10` | Registry (Shellbags) | Folder Visited in Explorer | Accessed E:\Stolen_Dump via GUI by dvance | `NTUSER.DAT\Shellbags` | 🔴 **ALERT** |
| `2026-10-04 18:29:12` | FileSystem (MFT) | FILE_CREATE | E:\Stolen_Dump\project_backup_v2.zip (User: dvance) - Copy attempted to Removable USB Drive (SanDisk) | `MFT-10535` | 🔴 **ALERT** |
| `2026-10-04 18:31:10` | Security EventLogs | Process Creation | Browser launched in incognito mode targeting file upload service [User: dvance] | `EventID: 4688` | 🔴 **ALERT** |
| `2026-10-04 18:31:10` | Registry (UserAssist) | Program Execution | Executed chrome.exe (RunCount: 4) | `NTUSER.DAT\UserAssist` | ⚪ Normal |
| `2026-10-04 18:31:12` | Network (Netflow) | Network Connection | 192.168.1.45:51204 -> 8.8.8.8:53 (DNS) - DNS Query for dropfile.to -> 185.220.101.42 - Bytes: 142 | `FLOW-8824` | 🔴 **ALERT** |
| `2026-10-04 18:31:12` | Network (PCAP) | DNS Query | Client 192.168.1.45 queried dropfile.to -> resolved to 185.220.101.42 | `lab_gateway_span_20261004.pcap` | 🔴 **ALERT** |
| `2026-10-04 18:31:14` | Network (Netflow) | Network Connection | 192.168.1.45:51206 -> 185.220.101.42:443 (TLS/HTTPS) - Initial HTTPS connection to dropfile.to landing page - Bytes: 48200 | `FLOW-8825` | 🔴 **ALERT** |
| `2026-10-04 18:31:20` | FileSystem (MFT) | FILE_ACCESS | C:\Users\Public\project_backup_v2.zip (User: dvance) - Staging archive selected in browser file upload picker | `MFT-10548` | 🔴 **ALERT** |
| `2026-10-04 18:34:10` | Network (PCAP) | DNS Query | Client 192.168.1.45 queried tempmail.org -> resolved to 104.21.34.12 | `lab_gateway_span_20261004.pcap` | 🔴 **ALERT** |
| `2026-10-04 18:35:35` | Network (Netflow) | Network Connection | 192.168.1.45:51240 -> 185.220.101.42:443 (TLS/HTTPS) - MASSIVE EXFILTRATION: Upload of 142.8 MB zip archive to dropfile.to - Bytes: 143120400 | `FLOW-8830` | 🔴 **ALERT** |
| `2026-10-04 18:35:35` | Network (PCAP) | TLS/App Session | 192.168.1.45 to 185.220.101.42 - SNI/Service: dropfile.to - Method: POST /api/upload | `lab_gateway_span_20261004.pcap` | 🔴 **ALERT** |
| `2026-10-04 18:35:40` | Browser Cache/Metadata | Browser File Upload / Exfiltration | Action: HTTP_MULTIPART_POST_UPLOAD to https://dropfile.to/api/upload - File: C:\Users\Public\project_backup_v2.zip (142840112 bytes). Response ID: 9x8K2L1q | `chrome_cache_metadata.json` | 🔴 **ALERT** |
| `2026-10-04 18:37:50` | Network (PCAP) | DNS Query | Client 192.168.1.78 queried mail.proton.me -> resolved to 185.70.40.185 | `lab_gateway_span_20261004.pcap` | 🔴 **ALERT** |
| `2026-10-04 18:38:00` | Network (Netflow) | Network Connection | 192.168.1.78:52100 -> 185.70.40.185:443 (TLS/HTTPS) - ProtonMail webmail connection to send exfiltration email - Bytes: 185400 | `FLOW-8835` | 🔴 **ALERT** |
| `2026-10-04 18:38:00` | Network (PCAP) | TLS/App Session | 192.168.1.78 to 185.70.40.185 - SNI/Service: mail.proton.me - Method: POST /api/messages | `lab_gateway_span_20261004.pcap` | 🔴 **ALERT** |
| `2026-10-04 18:38:05` | Email Artefact | Email Sent | From: David Vance <david.vance99@protonmail.com> To: "Dr. Jonathan Stern" <j.stern@competitor-lab.org> Subj: Final Drone AI Codebase & Trained Model Weights (Alex's Project) | Body preview: Dear Dr. Stern,

Following our discussion regarding the funded research fellowship in your autonomou... | `exfil_notification.eml` | 🔴 **ALERT** |
| `2026-10-04 18:40:15` | Registry (USBSTOR) | USB device removed | Device SanDisk Ultra USB 3.0 removed | `HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR` | 🔴 **ALERT** |
| `2026-10-04 18:41:48` | Security EventLogs | Process Creation | Command executed to delete staging zip file from disk [User: dvance] | `EventID: 4688` | 🔴 **ALERT** |
| `2026-10-04 18:41:48` | Registry (UserAssist) | Program Execution | Executed cmd.exe (RunCount: 3) | `NTUSER.DAT\UserAssist` | ⚪ Normal |
| `2026-10-04 18:41:50` | FileSystem (MFT) | FILE_DELETE | C:\Users\Public\project_backup_v2.zip (User: dvance) - Anti-forensics cleanup: Staging zip deleted via del command | `MFT-10560` | 🔴 **ALERT** |
| `2026-10-04 18:42:10` | Security EventLogs | Logoff | David Vance terminates RDP session after exfiltration [User: dvance] [IP: 192.168.1.78] | `EventID: 4634` | 🔴 **ALERT** |

## 6. Confidence Assessment & Limitations
- **Confidence Level:** **HIGH (98.5%)**
- **Rationale:** Direct multi-modal correlation: The RDP source IP, auth username, staging zip contents, network upload byte count, Chrome API response token, and RFC 5322 email headers form an unbroken, non-repudiable chain of custody.

**Identified Investigative Limitations:**
- Ephemeral upload on dropfile.to has a 24-hour expiration; retrieval from cloud provider requires external subpoena if expired.
- Incognito mode browsing prevented full on-disk cookie caching, though server response JSON was successfully extracted from active browser memory cache metadata.
- USB drive physical device was unmounted prior to forensic imaging; registry records confirm connection and folder access.

## 7. Recommended Remediation & Disciplinary Actions
1. **Revoke Credentials:** Immediately suspend user account `dvance` across all university directories, RDP gateways, and lab VPNs.
2. **Issue Takedown Notice:** Dispatch urgent copyright/DMCA takedown notice to `abuse@dropfile.to` requesting preservation and destruction of payload ID `9x8K2L1q`.
3. **Notify Legal & Target Lab:** Send formal legal cease-and-desist to `competitor-lab.org` and Dr. Jonathan Stern prohibiting retention or publication of Alex Mercer's research.
4. **Secure Lab Workstations:** Enforce network-level RDP isolation, disable USB mass-storage via Group Policy (GPO), and mandate multi-factor authentication (MFA) on interactive logons.