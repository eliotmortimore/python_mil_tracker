# Military Flight Tracker

This is a Python tool that monitors military aircraft worldwide using the Flightradar24 API, scores flights based on aircraft type and strategic location, and sends alerts (including WhatsApp messages via Twilio) for the most interesting flights.

---

## 🚀 Features
- Fetches live military flight data from Flightradar24  
- Scores flights by **aircraft type** and **high-interest locations**  
- Outputs a **clean, tabular summary** of the most interesting flight  
- Sends **WhatsApp alerts via Twilio**  
- Supports **automatic runs** (e.g., every 2 hours)  

---

## 🛠 Requirements
- **Python 3.8+**
- **Flightradar24 API key**
- **Twilio Account SID + Auth Token**
- **Twilio WhatsApp Sandbox enabled**

---

## ⚙️ Setup

### 1. Clone the Repository

git clone https://github.com/eliotmortimore/python_mil_tracker.git
cd python_mil_tracker

2. Create a Virtual Environment

python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

pip install -r requirements.txt

3. Configure API Keys & Secrets

You can either:

✅ Use a tokens.py file (not tracked by git):

TWILIO_SID = "your_twilio_sid_here"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token_here"
FR_24_API_KEY = "your_flightradar24_api_key_here"
TWILIO_PHONE = "whatsapp:+14155238886"   # Twilio sandbox number
MY_PHONE = "whatsapp:+1YOURNUMBER"       # Your WhatsApp number

✅ Or set environment variables for better security:

export TWILIO_SID="your_twilio_sid"
export TWILIO_AUTH_TOKEN="your_twilio_auth_token"
export FR_24_API_KEY="your_flightradar24_api_key"


⸻

4. Run the Script

python flight_finder.py

You’ll see a summary of the most interesting military flight and (if enabled) receive a WhatsApp alert.

⸻

📲 Twilio WhatsApp Sandbox Setup
	1.	Go to your Twilio Console → WhatsApp Sandbox
	2.	Send the join code (e.g., join snowy-dragon) to +14155238886 via WhatsApp
	3.	Once joined, you’ll receive alerts at your WhatsApp number

⸻

⏲ Auto-Run Every 2 Hours

Quick way (inside the script):

import time

while True:
    # Run the flight tracker
    time.sleep(7200)  # wait 2 hours

Or schedule with cron (macOS/Linux):

0 */2 * * * /path/to/python /path/to/flight_finder.py >> /path/to/log.txt 2>&1


⸻

🛡 GitHub Security
	•	tokens.py is listed in .gitignore so secrets aren’t pushed
	•	If you ever commit a secret by accident, rewrite Git history before pushing

⸻

✅ Future Plans
	•	ChatGPT flight pattern analysis → auto-generate an X/Twitter post
	•	More strategic region scoring (e.g., Arctic, Middle East, Pacific)
	•	Global tiling for more complete FR24 coverage

⸻

Maintained by Eliot Mortimore
