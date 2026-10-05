import csv
import json

def parse_network_logs(netflow_csv_path, pcap_summary_path):
    events = []

    with open(netflow_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append({
                "timestamp": row["Timestamp_UTC"],
                "source": "Network (Netflow)",
                "event": "Network Connection",
                "description": f"{row['SourceIP']}:{row['SourcePort']} -> {row['DestinationIP']}:{row['DestinationPort']} ({row['ApplicationProtocol']}) - {row['Notes']} - Bytes: {row['BytesTransferred']}",
                "reference": row["FlowID"]
            })

    with open(pcap_summary_path, "r", encoding="utf-8") as f:
        pcap_data = json.load(f)

        for dns in pcap_data.get("DNS_Queries", []):
             events.append({
                "timestamp": dns["Timestamp_UTC"],
                "source": "Network (PCAP)",
                "event": "DNS Query",
                "description": f"Client {dns['ClientIP']} queried {dns['Query']} -> resolved to {dns['AnswerIP']}",
                "reference": pcap_data["CaptureFile"]
            })

        for tls in pcap_data.get("TLS_SNI_Sessions", []):
             events.append({
                "timestamp": tls["Timestamp_UTC"],
                "source": "Network (PCAP)",
                "event": "TLS/App Session",
                "description": f"{tls.get('SrcIP')} to {tls.get('DstIP')} - SNI/Service: {tls.get('SNI', tls.get('Service', ''))} - Method: {tls.get('Method', 'N/A')}",
                "reference": pcap_data["CaptureFile"]
            })

    return events
