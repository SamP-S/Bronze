from datetime import date
import pandas as pd
from mailer import Mailer
from dotenv import load_dotenv
import os
from pathlib import Path
import numpy as np

CURRENT_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = CURRENT_DIR / ".env"
load_dotenv(envars)

# setup mail server/login
EMAIL_ADDRESS = os.getenv("AUTO_EMAIL")
EMAIL_PASSWORD = os.getenv("AUTO_PASSWORD")
PORT = 587  
EMAIL_SERVER = "smtp.gmail.com"

# setup mailer
MAILER = Mailer(EMAIL_SERVER, PORT, EMAIL_ADDRESS, EMAIL_PASSWORD)

# public GoogleSheets url BAD --> DONT LEAVE HERE
# SHEET_ID = "<GOOGLE_SHEET_ID>"
# SHEET_NAME = "<SHEET_NAME>"  
# URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_xl():
    # replace with google sheet api
    xl = pd.ExcelFile("Outstanding Quotes Testing.xlsx")
    return xl

def query_data_and_send_emails(xl):
    date_conv = {
        "In": pd.to_datetime,
        "Tender Closing Date": pd.to_datetime,
        "Out": pd.to_datetime,
    }
    df = pd.read_excel(xl, "2024 Commercial", converters=date_conv)
    reps = pd.read_excel(xl, "SCS Reps") 
    
    present = date.today()
    email_counter = 0
    print(df.columns)
    
    null_check = df["Out"].isnull()
    blacklist_check = df["Outcome"] != "Blacklisted"
    combined_check = null_check & blacklist_check
    
    quotes = df[combined_check]
    quotes = quotes.sort_values(by="In")
    
    for _, row in quotes.iterrows():
        print(row[["ID", "In", "Outcome", "Project Address", "Status"]])
        # if (present >= row["reminder_date"].date()) and (row["has_paid"] == "no"):
        #     MAILER.send_email(
        #         subject=f'[Coding Is Fun] Invoice: {row["invoice_no"]}',
        #         receiver_email=row["email"],
        #         name=row["name"],
        #         due_date=row["due_date"].strftime("%d, %b %Y"),  # example: 11, Aug 2022
        #         invoice_no=row["invoice_no"],
        #         amount=row["amount"],
        #     )
        #     email_counter += 1
        
    print(df.dtypes)
    print(quotes.shape)
    return f"Total Emails Sent: {email_counter}"


def main():
    print("start program")
    xl = load_xl() 
    query_data_and_send_emails(xl)

if __name__ == "__main__":
    main()
