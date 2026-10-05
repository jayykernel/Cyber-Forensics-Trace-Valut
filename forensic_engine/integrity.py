import hashlib
import os
import json

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def build_integrity_ledger(evidence_root, output_path=None):
    ledger = {}
    for root, _, files in os.walk(evidence_root):
        for file in files:
            full_path = os.path.join(root, file)
            ledger[full_path] = {
                "filename": file,
                "sha256": calculate_sha256(full_path),
                "size_bytes": os.path.getsize(full_path)
            }
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(ledger, f, indent=2)
    return ledger

create_integrity_ledger = build_integrity_ledger
