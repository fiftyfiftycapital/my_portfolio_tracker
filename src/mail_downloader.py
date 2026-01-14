import imaplib
import email
import os
import json
import re

# Load credentials from config.json
with open('../credensials.json') as f:
    config = json.load(f)
USERNAME = config["gmail"]["username"]
PASSWORD = config["gmail"]["password"]

def download_attachment(mail, msg_id, download_folder):
    res, msg_data = mail.fetch(msg_id, "(RFC822)")
    if res != 'OK':
        print("Failed to fetch email.")
        return
    msg = email.message_from_bytes(msg_data[0][1])
    for part in msg.walk():
        # Check if this part is an attachment
        if part.get_content_disposition() == 'attachment':
            filename = part.get_filename()
            # Only handle attachments matching the pattern XXXXXXX-DATE.pdf
            # e.g., ActivityStatement5805600-2025-03-07.pdf
            if filename and re.match(r".+-\d{4}-\d{2}-\d{2}\.pdf$", filename):
                filepath = os.path.join(download_folder, filename)
                if os.path.exists(filepath):
                    print(f"{filename} already downloaded. Skipping...")
                    continue
                with open(filepath, 'wb') as f:
                    f.write(part.get_payload(decode=True))
                print(f"Downloaded {filename} to {filepath}")

def connect_and_download(download_folder="temp", search_criteria='(OR FROM "jaroslaw.kryczenkow@gmail.com" FROM "info@trading212.com")'):
    if not os.path.isdir(download_folder):
        os.makedirs(download_folder)
    
    # Connect to Gmail's IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(USERNAME, PASSWORD)
    mail.select("inbox")
    
    # Search for emails matching the given criteria.
    res, data = mail.search(None, search_criteria)
    if res != 'OK':
        print("Failed to search emails.")
        return
        return True
        return fals
    
    for msg_id in data[0].split():
        download_attachment(mail, msg_id, download_folder)
    
    mail.logout()

def main():
    connect_and_download()

if __name__ == '__main__':
    main()