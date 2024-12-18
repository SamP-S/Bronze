import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def test_gmail():
	creds = None
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/gmail.compose"])
	else:
		print("ERROR: no \"tokens.json\" found. Try running 'python quickstart.py'")
		return None
	
	try:
		service = build("gmail", "v1", credentials=creds)
		results = service.users().labels().list(userId="me").execute()
		print(results)
		labels = results.get("labels", [])

		if not labels:
			print("No labels found.")
			return
		print("Labels:")
		for label in labels:
			print(label["name"])

	except HttpError as error:
		print(f"ERROR: test_gmail: {error}")

def test_sheets():
	creds = None
	if os.path.exists("token.json"):
		creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/drive.file"])
	else:
		print("ERROR: no \"tokens.json\" found. Try running 'python quickstart.py'")
		return None
	
	try:
		service = build("sheets", "v4", credentials=creds)

		SAMPLE_SPREADSHEET_ID = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
		SAMPLE_RANGE_NAME = "Class Data!A2:E"
		# Call the Sheets API
		sheet = service.spreadsheets()
		result = (
			sheet.values()
			.get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
			.execute()
		)
		values = result.get("values", [])
		if not values:
			print("No data found.")
			return
		print(f"Values: {values}")
		for row in values:
			print(f"Row: {row}")
   
	except HttpError as error:
		print(f"ERROR: test_gmail: {error}")

if __name__ == "__main__":
	test_gmail()
	test_sheets()