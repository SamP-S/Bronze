import os
from dotenv import load_dotenv
from pathlib import Path

import scs

# setup script globals
CURRENT_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
load_dotenv(CURRENT_DIR / ".env")

token_path = os.path.expanduser(os.environ.get("TOKEN_PATH"))
credentials_path = os.path.expanduser(os.environ.get("CREDENTIALS_PATH"))
creds = scs.google.GenToken(token_path, credentials_path, scs.google.SCOPES)
print(creds)

