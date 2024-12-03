import os
import base64
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# setup script globals
CURRENT_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
load_dotenv(CURRENT_DIR / ".env")
SCOPES = ["https://mail.google.com/"]

def gmail_send_message(sender:str, receiver:str):
    """Create and send an email message
    Print the message object
    Returns: Message object, including message id

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    if (sender is None) or (receiver is None):
        print("ERROR: sender or receiver is None")
        print(f"sender = {sender}; receiver = {receiver}")
        return None
    
    if os.path.exists(os.getenv("TEST_TOKEN_PATH")):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    else:
        print("ERROR: no \"tokens.json\" found. Try running 'python quickstart.py'")
        return None

    try:
        service = build("gmail", "v1", credentials=creds)
        
        # assembly message
        message = EmailMessage()
        message.set_content("This is a reminder to keep hydrated.")
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = "Automatic Email Reminder"
        
        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )
        print(f"Message: {send_message}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message


if __name__ == "__main__":
    sender = os.getenv("TEST_SENDER")
    receiver = os.getenv("TEST_RECIPIENT")
    gmail_send_message(sender, receiver)