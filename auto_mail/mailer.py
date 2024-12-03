import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

class Mailer:
    def __init__(self, mail_server, port, mail_address, mail_password):
        self.mail_server = mail_server
        self.port = port
        self.mail_address = mail_address
        self.mail_password = mail_password
        
        self.server = smtplib.SMTP(self.mail_server, self.port)
        self.success = True
        try:
            print("attempting mail server login")
            self.server.starttls()
            self.server.login(self.mail_address, self.mail_password)
            print("mail server login OK")
        except Exception as e:
                print(f"ERROR: Mail server failed: \n{e}")
                self.success = False
                self.err = e

    def send_email(self, subject, receiver_email, name):
        if (not self.success):
            print(f"WARNING: Can't send email from unsuccessful server login: \n{self.err}")
            return
        
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = formataddr(("Quote Auto Mailer", f"{self.mail_address}"))
        msg["To"] = receiver_email
        msg["BCC"] = self.mail_address

        msg.set_content(
            f"""\
            Hi {name},
            This is a reminder to chase the QUOTE DETAILS quote.
            Have a good day,
            Axel
            """
        )
        
        msg.add_alternative(
            f"""\
        <html>
        <body>
            <p>Hi {name},</p>
            <p>This is a reminder to chase the QUOTE DETAILS quote.</p>
            <p>Have a good day,</p>
            <p>Axel</p>
        </body>
        </html>
        """,
            subtype="html",
        )
        self.server.sendmail(self.mail_address, receiver_email, msg.as_string())
            
