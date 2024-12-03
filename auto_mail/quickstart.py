import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from test import test_gmail, test_sheets

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