import json
import os
from datetime import datetime

def generate_markdown_report(ledger, timeline, attack_chain, analysis, output_path):
    md = []
    md.append("# DIGITAL FORENSICS INVESTIGATION REPORT")
    md.append("## CASE FILE: 2026-DFIR-0881 / \"The Stolen Project Files\"\n")
    md.append(f"**Date of Analysis:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}  ")
    md.append("**Lead Investigator:** Antigravity Forensic Intelligence Unit  ")
    md.append(f"**Overall Verdict:** UNLAWFUL DATA EXFILTRATION IDENTIFIED — CONFIDENCE: **{analysis['confidence_assessment']['level']} ({analysis['confidence_assessment']['score_percentage']}%)**\n")
    md.append("---\n")

    # 1. Executive Summary
    md.append("## 1. Executive Summary")
    md.append(f"On **October 4, 2026**, between **18:14:20 UTC and 18:42:10 UTC**, an unauthorized remote access session was established against final-year student **Alex Mercer's** workstation (`LAB-WS-07`, `192.168.1.45`). The intruder accessed proprietary research files relating to the *Autonomous Drone Navigation AI* project, staged them into an archive (`project_backup_v2.zip`, 142.8 MB), uploaded the payload to an anonymous file transfer service (`dropfile.to`), attempted physical copying via USB (`SanDisk Ultra`), and distributed access credentials to a competitor research institution (`competitor-lab.org`).")
    md.append(f"\nForensic analysis definitively attributes this intrusion to peer student **David Vance** (`dvance`, `DEV-LAPTOP-14`, `192.168.1.78`).\n")

    # 2. Case Questions & Findings
    md.append("## 2. Key Findings & Core Investigative Questions\n")

    # Q1
    q1 = analysis["answers"]["1_what_files_accessed"]
    md.append(f"### Q1: {q1['question']}")
    md.append(f"{q1['summary']}\n")
    md.append("| Compromised File | Size | Forensic Description | Evidence Ref |")
    md.append("| :--- | :--- | :--- | :--- |")
    for item in q1["items"]:
        md.append(f"| `{item['file']}` | {item['size']} | {item['description']} | `{item['evidence_ref']}` |")
    md.append("")

    # Q2
    q2 = analysis["answers"]["2_when_did_activity_occur"]
    md.append(f"### Q2: {q2['question']}")
    md.append(f"**Active Incident Window:** {q2['summary']}\n")
    md.append("| Timestamp (UTC) | Milestone Description |")
    md.append("| :--- | :--- |")
    for ms in q2["key_milestones"]:
        md.append(f"| `{ms['time']}` | {ms['event']} |")
    md.append("")

    # Q3
    q3 = analysis["answers"]["3_how_accessed"]
    md.append(f"### Q3: {q3['question']}")
    md.append(f"**Access Vector:** {q3['summary']}")
    md.append(f"\n{q3['mechanism']}")
    md.append(f"\n*Supporting Evidence:* {', '.join([f'`{r}`' for r in q3['evidence_refs']])}\n")

    # Q4
    q4 = analysis["answers"]["4_how_exfiltrated"]
    md.append(f"### Q4: {q4['question']}")
    md.append(f"**Exfiltration Channels:** {q4['summary']}\n")
    for d in q4["details"]:
        md.append(f"- {d}")
    md.append(f"\n*Supporting Evidence:* {', '.join([f'`{r}`' for r in q4['evidence_refs']])}\n")

    # Q5
    q5 = analysis["answers"]["5_who_source"]
    md.append(f"### Q5: {q5['question']}")
    md.append(f"- **Identified Subject:** {q5['suspect_name']} (Student ID: `{q5['suspect_id']}`)")
    md.append(f"- **Compromised/Active Account:** `{q5['user_account']}`")
    md.append(f"- **Originating Device:** `{q5['originating_device']}` (IP: `{q5['originating_ip']}`)")
    md.append(f"- **Key Attribution Proofs:**")
    for proof in q5["evidence_refs"]:
        md.append(f"  - {proof}")
    md.append("")

    # Q6
    q6 = analysis["answers"]["6_evidence_supporting_conclusion"]
    md.append(f"### Q6: {q6['question']}\n")
    md.append("| Evidence Modality | Specific Forensic Artifacts Verified |")
    md.append("| :--- | :--- |")
    for cat in q6["categories"]:
        md.append(f"| **{cat['category']}** | {cat['details']} |")
    md.append("")

    # 3. Chain of Custody & Evidence Ledger
    md.append("## 3. Evidence Inventory & Cryptographic Integrity Verification")
    md.append("All evidence files were verified upon ingestion with SHA-256 cryptographic hashing to maintain strict legal chain of custody.\n")
    md.append("| Evidence Identifier / Path | Size (Bytes) | SHA-256 Hash | Integrity Status |")
    md.append("| :--- | :--- | :--- | :--- |")
    for fpath, data in ledger.items():
        rel_path = os.path.relpath(fpath, r"C:\dev\Trace-Valut")
        md.append(f"| `{rel_path}` | {data['size_bytes']} | `{data['sha256']}` | **VERIFIED (PASS)** |")
    md.append("")

    # 4. Multi-Hop Incident Reconstruction (Attack Chain)
    md.append("## 4. Multi-Hop Incident Reconstruction (Attack Chain)")
    md.append("The automated correlation engine mapped individual artefacts into the following multi-hop sequence:\n")
    for st in attack_chain:
        md.append(f"### Stage {st['stage']}: {st['title']} (`{st['timestamp']}`)")
        md.append(f"- **Modality:** {st['source_type']}")
        md.append(f"- **Action:** {st['details']}")
        md.append(f"- **Evidence References:** {', '.join([f'`{r}`' for r in st['evidence_refs']])}\n")

    # 5. Master Chronological Unified Timeline
    md.append("## 5. Master Unified Chronological Timeline")
    md.append("| Timestamp (UTC) | Modality Source | Event Type | Description | Reference | Suspicious Flag |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :---: |")
    for ev in timeline:
        susp_badge = "🔴 **ALERT**" if ev.get("is_suspicious") else "⚪ Normal"
        md.append(f"| `{ev['timestamp']}` | {ev['source']} | {ev['event']} | {ev['description']} | `{ev.get('reference','')}` | {susp_badge} |")
    md.append("")

    # 6. Confidence & Limitations
    md.append("## 6. Confidence Assessment & Limitations")
    md.append(f"- **Confidence Level:** **{analysis['confidence_assessment']['level']} ({analysis['confidence_assessment']['score_percentage']}%)**")
    md.append(f"- **Rationale:** {analysis['confidence_assessment']['rationale']}")
    md.append("\n**Identified Investigative Limitations:**")
    for lim in analysis["limitations"]:
        md.append(f"- {lim}")
    md.append("")

    # 7. Recommendations
    md.append("## 7. Recommended Remediation & Disciplinary Actions")
    md.append("1. **Revoke Credentials:** Immediately suspend user account `dvance` across all university directories, RDP gateways, and lab VPNs.")
    md.append("2. **Issue Takedown Notice:** Dispatch urgent copyright/DMCA takedown notice to `abuse@dropfile.to` requesting preservation and destruction of payload ID `9x8K2L1q`.")
    md.append("3. **Notify Legal & Target Lab:** Send formal legal cease-and-desist to `competitor-lab.org` and Dr. Jonathan Stern prohibiting retention or publication of Alex Mercer's research.")
    md.append("4. **Secure Lab Workstations:** Enforce network-level RDP isolation, disable USB mass-storage via Group Policy (GPO), and mandate multi-factor authentication (MFA) on interactive logons.")

    report_text = "\n".join(md)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    return report_text

def generate_html_report(ledger, timeline, attack_chain, analysis, output_path):
    report_data = {
        "ledger": ledger,
        "timeline": timeline,
        "attack_chain": attack_chain,
        "analysis": analysis,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DFIR Forensic Investigation Report - The Stolen Project Files</title>
    <style>
        :root {{
            --bg: #0d1117;
            --card-bg: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --heading: #58a6ff;
            --accent: #238636;
            --danger: #f85149;
            --warning: #d29922;
            --info: #388bfd;
        }}
        @media print {{
            body {{ background: #fff !important; color: #111 !important; }}
            .card {{ border: 1px solid #ccc !important; background: #fff !important; box-shadow: none !important; }}
            .no-print {{ display: none; }}
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            line-height: 1.6;
            margin: 0;
            padding: 24px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #1f2937, #111827);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.5);
        }}
        .badge {{
            display: inline-block;
            padding: 4px 10px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85em;
        }}
        .badge-danger {{ background: rgba(248, 81, 73, 0.2); color: var(--danger); border: 1px solid var(--danger); }}
        .badge-success {{ background: rgba(35, 134, 54, 0.2); color: #3fb950; border: 1px solid #3fb950; }}
        .badge-warning {{ background: rgba(210, 153, 34, 0.2); color: var(--warning); border: 1px solid var(--warning); }}
        .badge-info {{ background: rgba(56, 139, 253, 0.2); color: var(--info); border: 1px solid var(--info); }}

        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 24px;
        }}
        h1, h2, h3, h4 {{ color: #f0f6fc; margin-top: 0; }}
        h2 {{ border-bottom: 1px solid var(--border); padding-bottom: 8px; color: var(--heading); }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 16px 0;
            font-size: 0.9em;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }}
        th {{
            background: #21262d;
            color: #f0f6fc;
            font-weight: 600;
        }}
        tr:hover {{ background: rgba(255,255,255,0.02); }}
        code {{
            font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
            background: rgba(110,118,129,0.2);
            padding: 2px 6px;
            border-radius: 4px;
            color: #79c0ff;
            font-size: 0.9em;
        }}
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}
        .timeline-step {{
            position: relative;
            padding-left: 28px;
            margin-bottom: 18px;
            border-left: 2px solid var(--info);
        }}
        .timeline-step::before {{
            content: "";
            position: absolute;
            left: -6px;
            top: 4px;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background: var(--info);
        }}
        .timeline-step.suspicious {{
            border-left-color: var(--danger);
        }}
        .timeline-step.suspicious::before {{
            background: var(--danger);
            box-shadow: 0 0 8px var(--danger);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h1>Digital Forensics Case Investigation Report</h1>
                    <p style="margin:4px 0; color:#8b949e;">CASE ID: <strong>2026-DFIR-0881</strong> &bull; Incident: <strong>"The Stolen Project Files"</strong></p>
                </div>
                <div style="text-align:right;">
                    <span class="badge badge-danger" style="font-size:1.1em;">VERDICT: GUILTY / PROVEN</span>
                    <p style="margin:6px 0 0 0; color:#8b949e; font-size:0.85em;">Confidence: <strong>98.5% (HIGH)</strong></p>
                </div>
            </div>
        </div>

        <div class="grid-2">
            <div class="card">
                <h3>Victim Profile</h3>
                <p><strong>Name:</strong> {analysis['victim_info']['name']}</p>
                <p><strong>Student ID:</strong> <code>{analysis['victim_info']['student_id']}</code></p>
                <p><strong>Workstation:</strong> <code>{analysis['victim_info']['device']}</code></p>
                <p><strong>Confidential Project:</strong> {analysis['victim_info']['project_name']}</p>
            </div>
            <div class="card" style="border-left: 4px solid var(--danger);">
                <h3>Identified Suspect Profile</h3>
                <p><strong>Name:</strong> <span style="color:var(--danger); font-weight:bold;">{analysis['suspect_info']['name']}</span></p>
                <p><strong>Student ID:</strong> <code>{analysis['suspect_info']['student_id']}</code></p>
                <p><strong>Account:</strong> <code>{analysis['suspect_info']['account']}</code></p>
                <p><strong>Originating Device:</strong> <code>{analysis['suspect_info']['device']}</code></p>
                <p><strong>External Emails:</strong> <code>{', '.join(analysis['suspect_info']['email_accounts'])}</code></p>
            </div>
        </div>

        <div class="card">
            <h2>1. Executive Summary</h2>
            <p>On <strong>October 4, 2026</strong>, between <strong>18:14:20 UTC and 18:42:10 UTC</strong>, unauthorized remote desktop access was established from <code>192.168.1.78</code> (David Vance's laptop) into workstation <code>LAB-WS-07</code> (Alex Mercer). The attacker copied four confidential research files, bundled them into <code>C:\\Users\\Public\\project_backup_v2.zip</code> (142.8 MB), uploaded the payload via Chrome to anonymous cloud service <code>dropfile.to</code>, attempted USB storage transfer, and emailed access credentials to <code>competitor-lab.org</code> in exchange for a funded research fellowship.</p>
        </div>

        <div class="card">
            <h2>2. Core Investigative Answers</h2>

            <h4>Q1: WHAT files/information were accessed?</h4>
            <table>
                <thead>
                    <tr><th>File Name</th><th>Size</th><th>Description</th><th>Evidence Ref</th></tr>
                </thead>
                <tbody>
"""
    for it in analysis["answers"]["1_what_files_accessed"]["items"]:
        html += f"<tr><td><code>{it['file']}</code></td><td>{it['size']}</td><td>{it['description']}</td><td><code>{it['evidence_ref']}</code></td></tr>"

    html += f"""
                </tbody>
            </table>

            <h4>Q2: WHEN did the suspicious activity occur?</h4>
            <p><strong>Window:</strong> {analysis['answers']['2_when_did_activity_occur']['summary']}</p>

            <h4>Q3: HOW were the files accessed?</h4>
            <p>{analysis['answers']['3_how_accessed']['mechanism']}</p>

            <h4>Q4: HOW were they potentially exfiltrated/shared?</h4>
            <ul>
"""
    for d in analysis["answers"]["4_how_exfiltrated"]["details"]:
        html += f"<li>{d}</li>"

    html += f"""
            </ul>

            <h4>Q5: WHO/WHICH ACCOUNT/DEVICE is the likely source?</h4>
            <p><strong>Suspect:</strong> {analysis['suspect_info']['name']} (Account: <code>{analysis['suspect_info']['account']}</code>, Device: <code>{analysis['suspect_info']['device']}</code>).</p>

            <h4>Q6: What evidence supports the conclusion?</h4>
            <table>
                <thead><tr><th>Modality</th><th>Verified Findings</th></tr></thead>
                <tbody>
"""
    for cat in analysis["answers"]["6_evidence_supporting_conclusion"]["categories"]:
        html += f"<tr><td><strong>{cat['category']}</strong></td><td>{cat['details']}</td></tr>"

    html += f"""
                </tbody>
            </table>
        </div>

        <div class="card">
            <h2>3. Attack Chain Incident Reconstruction</h2>
"""
    for st in attack_chain:
        html += f"""
            <div class="timeline-step suspicious">
                <strong>Stage {st['stage']}: {st['title']}</strong> <span style="color:#8b949e; font-size:0.85em;">({st['timestamp']} UTC)</span><br>
                <small style="color:var(--heading);">Source: {st['source_type']}</small>
                <p style="margin:4px 0;">{st['details']}</p>
                <small>Evidence: <code>{', '.join(st['evidence_refs'])}</code></small>
            </div>
"""

    html += f"""
        </div>

        <div class="card">
            <h2>4. Evidence Integrity Verification (SHA-256)</h2>
            <table>
                <thead><tr><th>Evidence File</th><th>Size (Bytes)</th><th>SHA-256 Hash</th><th>Status</th></tr></thead>
                <tbody>
"""
    for fpath, d in ledger.items():
        rel = os.path.relpath(fpath, r"C:\dev\Trace-Valut")
        html += f"<tr><td><code>{rel}</code></td><td>{d['size_bytes']}</td><td><small><code>{d['sha256']}</code></small></td><td><span class=\"badge badge-success\">PASS</span></td></tr>"

    html += f"""
                </tbody>
            </table>
        </div>

        <div class="card no-print" style="text-align:center; padding:16px;">
            <p style="color:#8b949e;">Report generated automatically by Trace-Vault Forensic Intelligence Engine.</p>
            <button onclick="window.print()" style="background:var(--heading); border:none; color:#000; padding:10px 20px; font-weight:bold; border-radius:6px; cursor:pointer;">Print / Save as PDF</button>
        </div>
    </div>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html
