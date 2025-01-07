import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
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

# Scopes configures the permissions the OAuth2 token will have.
# Delete the "token.json" file to re-authenticate with new scopes.
SCOPES = [
	"https://mail.google.com/",						# all gmail perms
	"https://www.googleapis.com/auth/spreadsheets"	# all sheets only perms
]

def main():
	"""
	Configures the 'tokens.json' file for OAuth2 permissions for various Google APIs.
	"""
	creds = None
	# Check if the user already had a valid token.
	if os.path.exists("token.json"):
			creds = Credentials.from_authorized_user_file("token.json", SCOPES)
	# If no credentials available, ask user to give perms through OAuth2.
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
					"credentials.json", SCOPES
			)
			creds = flow.run_local_server(port=0)
		# Save the credentials as 'token.json' file.
		with open("token.json", "w") as token:
			token.write(creds.to_json())

if __name__ == "__main__":
	main()
	test_gmail()
	test_sheets()