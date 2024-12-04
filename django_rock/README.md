# [[<-]](../README.md) Internal Tool Website
## Summary
Django based website for hosting internal tools.

## Requirements
Requsted by Alex. - Quote Manager \
An internal website to manage quote requests from clients, send reminders to reps and provide useful statistics/summaries to track performance.
1. Manual input by estimators
2. Automated email reminders to chase contracts
3. Automatically blacklist & manage blacklist
4. Use google sheet backend
5. Fields:
	a. Highlight contracts won/lost	
	b. Allow multiple SCS Reps
	c. Use type sets but provide safe "null" values with appropriate warnings
7. New page per year
8. Allow create, edit and delete contracts
9. Support various summary creation.

## Usage
Install the dependencies using requirements.txt
``` bash
python -m pip install -r "requirements.txt"
```