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


class GoogleAPI:
        
    @staticmethod
    def load_credentials(tokens_path:str, scopes:list):
        """
        Loads credentials from existing tokens file.
        Attempts to add scopes to credentials for needed permissions.

        Args:
            tokens_path (str): path to 'token.json' file
            scopes (list): list of google scopes needed to enable API perms

        Returns:
            google.oauth2.credentials or None : return credential object or None if failed.
        """
        try:
            return Credentials.from_authorized_user_file(tokens_path, scopes)
        except Exception as e:
            print("ERROR: GoogleAPI.load_credentials: ", e)
            return None

    
    mail_scope = ["https://mail.google.com/"]

    def __init__(self, tokens_path:str, sender:str):
        self.sender = sender
        self.tokens_path = tokens_path
        self.creds = self.load_credentials(self.tokens_path, self.mail_scope)
        self.success = False
        if (self.creds is not None and self.sender is not None):
            self.success = True
        else:
            print("ERROR: Can't load credentials")
            self.service = build("gmail", "v1", credentials=self.creds)
                
    def send_mail(self, receiver:str, subject:str, body:str):
        """
        Create and send an email message
        Prints the message object
        Returns: Message object or None if failed.
        """
        if (self.sender is None) or (receiver is None) or (body is None):
            print("ERROR: an args is None")
            print(f"sender = {self.sender};\n receiver = {receiver};\n body = {body};")
            return None

        try:
            service = build("gmail", "v1", credentials=self.creds)
            
            # assembly message
            message = EmailMessage()
            message.set_content("This is a reminder to keep hydrated.")
            message["From"] = self.sender
            message["To"] = receiver
            message["Subject"] = subject
            
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
    
# class SheetsAPI:
    

if __name__ == "__main__":
    # sender = os.getenv("SENDER_EMAIL")
    # receiver = os.getenv("RECEIVER_EMAIL")
    # tokens_path = os.getenv("TEST_TOKEN_PATH")
    
    # gmail = GoogleAPI(tokens_path, sender)
    # gmail.send_mail(
    #     receiver,
    #     "Automatic Email Reminder",
    #     "This is a reminder to keep hydrated."
    # )
    
    GoogleAPI.load_credentials("bad_path.json", ["https://mail.google.com/"])