# Automated Email Reminder System
Google API based email reminder system. Utilising Google API and OAuth.

## Requirements
Install the dependencies using requirements.txt
``` bash
python -m pip install -r "requirements.txt"
```
Download client OAuth as "credentials.json" from [Google Cloud Console](https://console.cloud.google.com/apis/credentials). Then run python script to get authorize the google account to be used with the OAuth to allow the software to use the given account through the Gmail api. Do **NOT** delete the "tokens.json" or "credentials.json" from local and do **NOT** push these files to github.
``` bash
python quickstart.py"
```

## Summary
Wraps the Google API for Gmail and Sheets as a single interface.


<!-- ## Environment Variables
To run this project, you will need to add the following environment variables to your .env file <br/>
`AUTO_EMAIL`
`AUTO_PASSWORD` -->
