import email
from email import policy
import glob
import os
from email.utils import parsedate_to_datetime

def parse_eml_files(email_dir):
    events = []

    for filepath in glob.glob(os.path.join(email_dir, "*.eml")):
        with open(filepath, "r", encoding="utf-8") as f:
            msg = email.message_from_file(f, policy=policy.default)

            # Format datetime
            dt = parsedate_to_datetime(msg.get("Date"))
            timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore')

            preview = body.replace("\\n", " ")[:100] + "..."

            events.append({
                "timestamp": timestamp,
                "source": "Email Artefact",
                "event": "Email Sent",
                "description": f"From: {msg.get('From')} To: {msg.get('To')} Subj: {msg.get('Subject')} | Body preview: {preview.strip()}",
                "reference": os.path.basename(filepath)
            })
    return events
