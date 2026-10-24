import google.auth
import gspread

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEET_NAME = 'Recruiters'

creds, _ = google.auth.default(scopes=SCOPES)
gc = gspread.authorize(creds)
sh = gc.open(SHEET_NAME)
worksheet = sh.worksheet("Contacts")
print(worksheet.get_all_values())