import requests
import json
from tabulate import tabulate

#Commented out token import to work with Render.com [Uncomment if you are running locally}
#from tokens import TWILIO_AUTH_TOKEN, TWILIO_SID, FR_24_API_ENDPOINT, FR_24_API_KEY, TWILIO_PHONE, MY_PHONE, OPENAI_API_KEY


def main():
    # ✅ Define interesting zones before anything else
    interesting_zones = [
        {"name": "Taiwan Strait", "bounds": [22.0, 26.0, 118.0, 122.5], "score": 5},
        {"name": "South China Sea", "bounds": [5.0, 20.0, 110.0, 122.0], "score": 5},
        {"name": "Black Sea / Crimea", "bounds": [40.0, 47.0, 27.0, 38.0], "score": 4},
        {"name": "Kaliningrad / Baltic Sea", "bounds": [53.0, 57.0, 19.0, 23.0], "score": 4},
        {"name": "Persian Gulf", "bounds": [23.0, 28.0, 50.0, 58.0], "score": 5},
        {"name": "Korean DMZ", "bounds": [37.0, 39.5, 125.0, 128.0], "score": 4},
        {"name": "Syria / East Med", "bounds": [32.0, 38.0, 34.0, 42.0], "score": 4},
        {"name": "Barents Sea", "bounds": [68.0, 78.0, 15.0, 50.0], "score": 4},
        {"name": "GIUK Gap", "bounds": [58.0, 70.0, -30.0, 0.0], "score": 4},
        {"name": "Diego Garcia", "bounds": [-10.0, -5.0, 70.0, 75.0], "score": 3}
    ]

    def score_location(lat, lon):
        for zone in interesting_zones:
            lat_min, lat_max, lon_min, lon_max = zone["bounds"]
            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                return zone["score"]
        return 0

    url = FR_24_API_ENDPOINT
    params = {'bounds': '90,-90,-180,180'}
    headers = {
        "Accept": "application/json",
        "Accept-Version": "v1",
        "Authorization": f"Bearer {FR_24_API_KEY}"
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        flights_list = data.get("data", [])
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        flights_list = []
    except Exception as err:
        print(f"An error occurred: {err}")
        flights_list = []

    scores = []
    for flight in flights_list:
        score = 0
        plane_type = flight.get("type", "").upper()
        callsign = flight.get("callsign")
        lat = flight.get("lat")
        lon = flight.get("lon")

        if plane_type in ["B52", "F22", "F35", "U2", "E3TF", "RC135"]:
            score += 5
        elif plane_type in ["P8", "EUFI", "F16", "F15", "F18", "C5", "C5M", "Q4"]:
            score += 4
        elif plane_type in ["K35R", "C130", "C30J", "P3", "C17"]:
            score += 3
        elif plane_type in ["P3", "B762"]:
            score += 2
        elif plane_type in ["TEX2"]:
            score += 1

        location_score = 0
        if lat is not None and lon is not None:
            location_score = score_location(lat, lon)

        total_score = score + location_score

        scores.append({
            "plane_type": plane_type,
            "location_score": location_score,
            "aircraft_score": score,
            "total_score": total_score,
            "flight": flight
        })

    if scores:
        top_flight_data = max(scores, key=lambda x: x["total_score"])
        flight_info = top_flight_data["flight"]
        flight_hex = flight_info["hex"]
        callsign = flight_info.get("callsign")
        fr24_url = f"https://www.flightradar24.com/{flight_hex}" if flight_hex else "No link available"

        columns = [
            ["Plane Type", top_flight_data["plane_type"]],
            ["Aircraft Score", top_flight_data["aircraft_score"]],
            ["Location Score", top_flight_data["location_score"]],
            ["Total Score", top_flight_data["total_score"]],
            ["Callsign", flight_info.get("callsign")],
            ["Origin", flight_info.get("orig_iata")],
            ["FR24 URL", fr24_url]
        ]

        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)

        flight_context_text = f"""
        Aircraft: {top_flight_data["plane_type"]}
        Callsign: {flight_info.get("callsign")}
        Origin: {flight_info.get("orig_iata")}
        FR24 Link: {fr24_url}

        Write 1–2 short, engaging sentences like a tweet for aviation watchers explaining why this flight might be interesting.
        """
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an aviation OSINT expert who writes short, engaging tweets about unusual military flights."},
                {"role": "user", "content": flight_context_text}
            ]
        )

        tweet_text = response.choices[0].message.content
        print("Generated Tweet:", tweet_text)

        message_body = f"{tweet_text}\n\nTrack it live: {fr24_url}"
        print("Sending WhatsApp message:", message_body)

        from twilio.rest import Client
        account_sid = TWILIO_SID
        auth_token = TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message_body,
            from_=f"whatsapp:{TWILIO_PHONE}",
            to=f"whatsapp:{MY_PHONE}"
        )
        print("WhatsApp message sent! SID:", message.sid)

        print(tabulate(columns, headers=["Field", "Value"], tablefmt="github"))
    else:
        print("No flights to evaluate.")

#Time function
if __name__ == "__main__":
    print("🚀 Running flight tracker...")
    main()
    print("✅ Finished run.")
