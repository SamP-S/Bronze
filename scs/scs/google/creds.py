import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes configures the permissions the OAuth2 token will have.
# Delete the "token.json" file to re-authenticate with new scopes.
# TODO: consider if scopes should be set in .env or here or at credential functions (current).
SCOPES_ALL = [
	"https://mail.google.com/",						# all gmail perms
	"https://www.googleapis.com/auth/spreadsheets"	# all sheets only perms
]

SCOPES_MAIL_ONLY = [
	"https://mail.google.com/",						# all gmail perms
]

SCOPES_SHEETS_ONLY = [
	"https://www.googleapis.com/auth/spreadsheets"	# all sheets only perms
]

SCOPES_READ_ONLY = [
	"https://www.googleapis.com/auth/gmail.readonly",		# read-only gmail perms
 	"https://www.googleapis.com/auth/spreadsheets.readonly"	# read-only sheets perms
]

# default
SCOPES = SCOPES_ALL

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
def LoadToken(token_path: str, scopes:list=SCOPES) -> Credentials:
    if os.path.exists(token_path):
        return Credentials.from_authorized_user_file(token_path, scopes)
    else:
        print(f"ERROR: Token not found. Try generate new credentials.\n \"{token_path}\"")

# Generate credentials for user from "credentials.json" file from google cloud dashboard.
# If no existing credentials are available, ask user to give permissions through OAuth2.
def GenToken(token_path:str, credentials_path:str, scopes:list=SCOPES) -> Credentials:
    creds = LoadToken(token_path, scopes)
    
    # If no credentials available, ask user to give perms through OAuth2.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes)
            creds = flow.run_local_server(port=0)
            
        # Save new token to file.
        with open(token_path, "w") as token:
            token.write(creds.to_json())
    else:
        print(f"INFO: Existing valid credentials exist. Skipping OAuth2 request...")
    return creds