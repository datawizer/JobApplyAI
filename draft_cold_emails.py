import base64
from email.mime.text import MIMEText
import google.auth
import gspread
from googleapiclient.discovery import build

# Define scopes
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.send"
]

# Load credentials from the configured Google Application Default Credentials.
creds, _ = google.auth.default(scopes=SCOPES)

# Authenticate for Google Sheets and Gmail
gc = gspread.authorize(creds)
gmail_service = build('gmail', 'v1', credentials=creds)

# Open the spreadsheet and worksheets
spreadsheet = gc.open("Recruiters")
contacts_sheet = spreadsheet.worksheet("Contacts")
done_sheet = spreadsheet.worksheet("Done")

# Read data from Contacts (excluding headers)
contacts_data = contacts_sheet.get_all_values()
headers = contacts_data[0]
rows = contacts_data[1:]

# Process each row
for idx, row in enumerate(rows, start=2):  # start=2 to match row number in sheet
    name, email, company = row

    if not email:
        print(f"Skipping empty email row at {idx}")
        continue

    subject = f"Interest in opportunities at {company}"
    body = f"""
    Dear {name},

    I hope this message finds you well. I’m reaching out to express my interest in opportunities at {company}.
    With a background in data and analytics, I’d love to explore how I can contribute to your team.

    Please let me know if there’s a good time to connect.

    Best regards,  
    Datawizer  
    """

    # Create email
    message = MIMEText(body)
    message['to'] = email
    message['subject'] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    email_message = {
        'raw': raw
    }

    try:
        # Create a draft email
        gmail_service.users().drafts().create(userId="me", body={"message": email_message}).execute()
        print(f"Draft created for {name} ({email})")

        # Append to 'Done' sheet
        done_sheet.append_row(row)

        # Delete from 'Contacts' sheet
        contacts_sheet.delete_rows(idx)

    except Exception as e:
        print(f"Failed to process {name} ({email}) - {e}")
