# Trace-Vault: Automated Digital Forensics & Incident Response Suite
### Case File: `2026-DFIR-0881` | *"The Stolen Project Files"*

---

## 🎯 Executive Overview & Case Resolution

**Trace-Vault** is a digital forensics investigation pipeline and interactive analyst suite designed for fast, forensically sound triage of multi-modal evidence.

In the case of **"The Stolen Project Files"**, a final-year student's (**Alex Mercer**, `CS-2026-8841`) proprietary *Autonomous Drone Navigation AI (Transformer-LiDAR)* research was illicitly accessed and exfiltrated. 

The Trace-Vault pipeline systematically ingested, verified, parsed, correlated, and reconstructed the incident across **6 independent forensic modalities**, attributing the intrusion with **98.5% High Confidence** to peer student **David Vance** (`dvance`, `CS-2026-9012`).

---

## 🔍 The 6 Core Investigative Answers

| # | Core Question | Forensic Finding / Resolution | Supporting Evidence |
|---|---|---|---|
| **Q1** | **WHAT** files were accessed? | Four confidential project files totaling **142.8 MB**: <br>1. `drone_nav_core.py` (Algorithm code, 1.4 KB)<br>2. `neural_weights_v4.bin` (Trained model weights, 50.0 MB)<br>3. `dataset_lidar_final.parquet` (LiDAR point cloud data, 78.1 MB)<br>4. `project_final_report.docx` (Dissertation & patent draft, 441.4 KB) | `MFT-10512` to `MFT-10515`, `CARVED-ZIP-001` unallocated metadata manifest. |
| **Q2** | **WHEN** did the activity occur? | **October 4, 2026 between 18:14:20 UTC and 18:42:10 UTC** (~28 minutes active incident window). | Timeline bounded by RDP logon at `18:14:22 UTC` and RDP logoff at `18:42:10 UTC`. |
| **Q3** | **HOW** were the files accessed? | **Lateral Remote Desktop Protocol (RDP) session (Logon Type 10)** from suspect laptop `192.168.1.78` into `LAB-WS-07` (`192.168.1.45:3389`), followed by file archiving into `C:\Users\Public\project_backup_v2.zip` using `7z.exe`. | Windows Security Event ID `4624` (Logon Type 10), Netflow `FLOW-8810`, Event ID `4688` (`7z.exe`). |
| **Q4** | **HOW** were they exfiltrated/shared? | **Triple-channel exfiltration:**<br>1. *Primary:* 143.1 MB HTTPS upload to anonymous file drop `dropfile.to/api/upload` (IP: `185.220.101.42:443`).<br>2. *Secondary:* RFC 5322 EML email dispatched from `david.vance99@protonmail.com` to `j.stern@competitor-lab.org` with download token & password `droneAI_v4_secret`.<br>3. *Ancillary:* Copy attempted to SanDisk Ultra USB (`E:\Stolen_Dump\`). | `chrome_cache_metadata.json`, Netflow `FLOW-8830`, `exfil_notification.eml`, `USBSTOR` registry. |
| **Q5** | **WHO / WHICH ACCOUNT / DEVICE** is the source? | **Suspect:** David Vance (`CS-2026-9012`)<br>**Account:** `LAB-DOMAIN\dvance`<br>**Device:** `DEV-LAPTOP-14` (IP: `192.168.1.78`, MAC: `00:E0:4C:68:02:11`) | Event ID 4624 `TargetUserName: dvance`, `WorkstationName: DEV-LAPTOP-14`, Netflow source IP `192.168.1.78`, RFC 5322 `X-Originating-IP: [192.168.1.78]`. |
| **Q6** | **WHAT EVIDENCE** supports the conclusion? | Multi-hop cross-correlation across **6 distinct modalities**: Auth Logs, NTFS MFT, SQLite Browser History, RFC 5322 Email headers, Netflow/PCAP traffic, and USB Registry. | 100% SHA-256 integrity-verified evidence chain; zero temporal or semantic discrepancies. |

---

## 🔗 Reconstructed Multi-Hop Attack Chain

```
[ Stage 1: Ingress ] ────► [ Stage 2: Traversal ] ────► [ Stage 3: Staging ] ────► [ Stage 4: Physical USB ]
  RDP from 192.168.1.78     Explorer traversal of        7z.exe creates 142.8 MB     SanDisk Ultra inserted;
  Logon Type 10 (dvance)    C:\Projects\FinalYear_...    project_backup_v2.zip       copied to E:\Stolen_Dump
  (18:14:20 UTC)            (18:17:45 UTC)               (18:22:10 UTC)              (18:28:30 UTC)
                                                                                            │
                                                                                            ▼
[ Stage 7: Anti-Forensics ] ◄── [ Stage 6: Distribution ] ◄── [ Stage 5: Cloud Exfiltration ]
  cmd.exe del staging zip        ProtonMail email sent to      Chrome uploads 143.1 MB to
  RDP session terminated         j.stern@competitor-lab.org    dropfile.to (185.220.101.42)
  (18:41:50 UTC)                 (18:38:05 UTC)                (18:35:40 UTC)
```

---

## 🏗️ Architecture & Pipeline Components

```
Trace-Valut/
├── evidence/                            # Multi-modal raw simulated forensic artefacts (Read-Only)
│   ├── filesystem/                      # NTFS MFT timeline & unallocated carved zip metadata
│   ├── auth_logs/                       # Windows Event Logs (Security.evtx) & System Registry
│   ├── browser/                         # Chrome history SQLite database & upload cache metadata
│   ├── email/                           # RFC 5322 EML emails with full headers & DKIM
│   └── network/                         # Netflow connection logs & PCAP DNS/TLS session traces
├── forensic_engine/                     # Modular Forensics Engine
│   ├── integrity.py                     # SHA-256 cryptographic hashing & Chain of Custody ledger
│   ├── extractors/                      # Modality-specific artifact parsers (FS, Auth, Browser, Email, Net)
│   ├── timeline.py                      # Chronological sorting & suspicious heuristic tagging
│   ├── correlator.py                    # Multi-hop automated attack chain correlation engine
│   ├── incident_analyzer.py             # Incident synthesis, confidence calculation, & Q1-Q6 resolution
│   └── report_generator.py              # Automated legal Markdown & printable HTML report builders
├── dashboard/                           # Single-Page Forensic Investigator Suite
│   └── index.html                       # Standalone interactive UI (Timeline, Ledger, Artifact Viewers)
├── reports/                             # Generated forensic case outputs
│   ├── integrity_ledger.json            # Cryptographic SHA-256 evidence ledger
│   ├── forensic_summary.json            # Master machine-readable incident synthesis
│   ├── FORENSIC_INVESTIGATION_REPORT.md # Formal Markdown forensic report
│   └── Forensic_Report.html             # High-fidelity printable forensic report
├── run_investigation.py                 # Master CLI orchestrator (Executes full end-to-end pipeline)
├── test_pipeline.py                     # Comprehensive automated unit & integration test suite
└── create_simulated_evidence.py         # Forensic evidence generator (reproducible multi-modal dataset)
```

---

## 🚀 Quickstart Guide

### 1. Run the End-to-End Investigation Pipeline
Execute the full forensic pipeline from ingestion to report generation with a single command:
```bash
python run_investigation.py
```

### 2. Run the Verification Test Suite
Verify that evidence hashing, parsing, correlation, and reports pass all test cases:
```bash
python test_pipeline.py
```

### 3. Open the Interactive Investigator Dashboard
Open `dashboard/index.html` in any web browser (no local web server or internet connection required; fully zero-dependency):
- **Windows (PowerShell):** `Start-Process dashboard/index.html`
- Or simply double-click `dashboard/index.html` in Windows Explorer.

---

## 👨‍⚖️ How to Demonstrate This to Judges

When presenting this solution to the judges, follow this **3-minute high-impact walkthrough**:

1. **Step 1: Execute the Pipeline Live (`python run_investigation.py`)**
   - Point out the **6 sequential pipeline phases** executing live in the terminal.
   - Show that **14 raw evidence files** are hashed with **SHA-256** to establish strict chain of custody without modifying originals.
   - Highlight the terminal output summarizing the answers to all **6 core case questions**.

2. **Step 2: Demonstrate the Interactive Dashboard (`dashboard/index.html`)**
   - **Tab 1 (Overview & 6 Questions):** Show the side-by-side Victim vs. Suspect profiles and the detailed breakdown answering What, When, How, Who, and Evidence.
   - **Tab 2 (Attack Chain):** Show the 7-stage visual incident reconstruction linking ingress to anti-forensics.
   - **Tab 3 (Master Timeline):** Filter by *"Suspicious / Incident Events Only"* to show how anomaly detection flags suspicious activity across Windows logs, MFT, network flows, and browser history.
   - **Tab 4 (Evidence Ledger):** Show the tamper-proof cryptographic SHA-256 ledger proving data integrity.
   - **Tab 5-7 (Deep Dives):** Show the intercepted **ProtonMail RFC 5322 EML email** (identifying David Vance offering the files in exchange for a fellowship), the **Chrome multipart POST upload response** from `dropfile.to`, and the **143.1 MB Netflow flow record**.

3. **Step 3: Run the Test Suite (`python test_pipeline.py`)**
   - Show all 7 unit and integration tests passing (`Ran 7 tests ... OK`), demonstrating software reliability, deterministic correlation, and defensive data integrity.
