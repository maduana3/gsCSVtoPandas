from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

CREDS = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '' #sheetID goes here
DATA_TO_PULL = '' #sheetname goes here

def pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL,CREDS):
    service = build('sheets', 'v4', credentials=CREDS)
    sheet = service.spreadsheets()
    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=DATA_TO_PULL).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
    else:
        rows = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=DATA_TO_PULL).execute()
        data = rows.get('values')
        print("COMPLETE: Data copied")
        return data

data = pull_sheet_data(SCOPES,SPREADSHEET_ID,DATA_TO_PULL,CREDS)
df = pd.DataFrame(data[1:], columns=data[0])
df.to_csv(r'\histData.csv', index=False, header=False)

print(df)
