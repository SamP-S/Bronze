import os
from pathlib import Path
from dotenv import load_dotenv

# setup script globals
CURRENT_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
load_dotenv(CURRENT_DIR / ".env")



creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    scopes = ["https://www.googleapis.com/auth/gmail.compose"]
    creds = Credentials.from_authorized_user_file("token.json", scopes)
else:
    print("ERROR: no \"tokens.json\" found. Try running 'python quickstart.py'")
    return None


if (sender is None) or (receiver is None):
    print("ERROR: sender or receiver is None")
    print(f"sender = {sender}; receiver = {receiver}")
    return None

if os.path.exists(os.getenv("TEST_TOKEN_PATH")):
    scopes = ["https://mail.google.com/"]
    creds = Credentials.from_authorized_user_file("token.json", scopes)
else:
    print("ERROR: no \"tokens.json\" found. Try running 'python quickstart.py'")
    return None