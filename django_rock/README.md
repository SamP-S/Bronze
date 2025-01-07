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

## Todo
- Converge file converters to single pages
- Merge file converters into single autodetecting converter


## Usage
Install the dependencies using requirements.txt
``` bash
python -m pip install -r "requirements.txt"
```

## Deployment
Deployment on raspberry pi zero w for very cheap hosting within local network.

#### Todo:
- Use duckdns.org as hosted DNS webdomain, easier to share than hostname.
- Utilise git webhooks and jenkins to ensure webserver is latest
- Implement testing and upkeep bot to notify if latest is broken

#### Issues:
- Only local network access, as without proper authentication and network firewall control it will be a security risk.
- Only 8GB Micro SD card so very limited storage.
- Networking speed and SD card is slow.


## Alternative Deployment Options
#### [python anywhere](https://pythonanywhere.com)
- £5 a month subscription for a single web app (single website)
- 1GB storage
- 2000s CPU time per day as priority (33.33 minutes) the in the tarpit
- "enough power to run a 100,000 hit/day site"

#### [google cloud](https://cloud.google.com)
- likely uses "App engine"
- free tier but unclear what
- wants you to do it their way
- fucking confusing

#### [aws](https://aws.amazon.com/free)
- offers elastic cloud (EC2) where you run virtual servers to scale up/down
- free 12 months of 750 hours ec2

#### [raspberry pi zero w](https://raspberrypi.org)
- pi zero 2 is £15
- limited storage unless v big sd card
- slow networking
- needs lots of extras e.g. cooling, power supply, ethernet adapter

