from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd


# public GoogleSheets url BAD --> DONT LEAVE HERE
# SHEET_ID = "<GOOGLE_SHEET_ID>"
# SHEET_NAME = "<SHEET_NAME>"  
# URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
SAMPLE_RANGE_NAME = "Class Data!A:Z"

# TODO: support many more parameters
# Read in a google sheet from api into pandas dataframe of raw data for local read usage
def LoadSheet(creds:Credentials, sheet_id:str, range:str, valueRenderOption="UNFORMATTED_VALUE", headerRow=None) -> pd.DataFrame:
    try:
        service = build("sheets", "v4", credentials=creds)
        
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=sheet_id, range=range, valueRenderOption=valueRenderOption)
            .execute()
        )
        values = result.get("values", [])
        if not values:
            print(f"WARNING {__name__}: No data found. @ {sheet_id} in {range}")
            return None
        
        # TODO: implement better catch guards
        if headerRow is None:
            return pd.DataFrame(values)
        else:            
            return pd.DataFrame(values[headerRow+1:], columns=values[headerRow])
            
        
    except HttpError as error:
        print(f"ERROR {__name__}: {error}")
        return None