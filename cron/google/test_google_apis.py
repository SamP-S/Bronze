import os
from dotenv import load_dotenv
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import scs


def test_gmail(creds):
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
  
  
def test_sheets(creds):
	SAMPLE_SPREADSHEET_ID = scs.google.SAMPLE_SPREADSHEET_ID
	SAMPLE_RANGE_NAME = scs.google.SAMPLE_RANGE_NAME
	df = scs.google.LoadSheet(creds, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
	print(df)


def main():
	"""
	Configures the 'tokens.json' file for OAuth2 permissions for various Google APIs.
	"""
 
	# setup script globals
	CURRENT_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
	load_dotenv(CURRENT_DIR / ".env")
 
	token_path = os.path.expanduser(os.environ.get("TOKEN_PATH"))
	credentials_path = os.path.expanduser(os.environ.get("CREDENTIALS_PATH"))
	creds = scs.google.GenToken(token_path, credentials_path, scs.google.SCOPES)
	print(creds)
	if (creds is None) or not creds.valid:
		print("ERROR: Failed to generate credentials. FAILED.")
		return

	test_gmail(creds)
	test_sheets(creds)
	
if __name__ == "__main__":
	main()