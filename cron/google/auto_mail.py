import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from datetime import date, timedelta

import scs

# convert from int date count from the epoch if a date is set
def convert_to_datetime(x):
    try:
        return timedelta(x) + date(1899, 12, 30)
    except:
        return pd.NaT

# setup script globals
CURRENT_DIR = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
load_dotenv(CURRENT_DIR / ".env")

token_path = os.path.expanduser(os.environ.get("TOKEN_PATH"))
credentials_path = os.path.expanduser(os.environ.get("CREDENTIALS_PATH"))
creds = scs.google.GenToken(token_path, credentials_path, scs.google.SCOPES)

SHEET_ID = "14xyE3zIrB1UHdPaU2-acbyQ3s00HWvFgrAKOsqlWulg"
RANGE = "2024 Commercial!A:Z"
df = scs.google.LoadSheet(creds, SHEET_ID, RANGE, headerRow=1)
df["In"] = pd.to_datetime(df["In"].apply(convert_to_datetime))
df["Tender Closing Date"] = pd.to_datetime(df["Tender Closing Date"].apply(convert_to_datetime))
df["Out"] = pd.to_datetime(df["Out"].apply(convert_to_datetime))


df = df[df["Out"].isna() & (df["Blacklisted"] != "y")]

today = date.today()
reminder_threshold = today + timedelta(days=3)
print(reminder_threshold)
df = df[df["Tender Closing Date"] <= pd.Timestamp(reminder_threshold)]
print(df)
print(df.shape)

if df.shape[0] <= 0:
    print("INFO: No reminders to send. Good Job. Exiting...")
    exit()
    
def days_to_emoji(days):
    if days <= 0:
        return "🔴"
    elif days <= 1:
        return "🟡"
    else:
        return "🟢"

# msg = "Hi,\n\nThe following tenders are closing <b>soon</b>:\n\n"
# for index, row in df.iterrows():
#     days_left = (row["Tender Closing Date"] - pd.Timestamp(today)).days
#     msg += f"<i>{row["Contractor"]}</i>\t@\t<b>{row["Project Address"]}</b>: {days_left} days.\n"
# msg += "\n\n Send Quotes ASAP.\n"

msg = "Hi,\n\nThe following tenders are closing **soon**:\n\n"
for index, row in df.iterrows():
    days_left = (row["Tender Closing Date"] - pd.Timestamp(today)).days
    msg += f"{row["Contractor"]}  @  {row["Project Address"]}: \t{days_to_emoji(days_left)} {days_left} days.\n"
msg += "\n\n Send Quotes ASAP.\n"

scs.google.gmail.SendEmail(
    creds, 
    "sam@southcoaststone.com", 
    "sam@southcoaststone.com", 
    "Tender Closing Reminder",
    msg
)
