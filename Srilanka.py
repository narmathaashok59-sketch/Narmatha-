import os
import sys
import requests
import smtplib
from email.mime.text import MIMEText

# Ensure UTF-8 output for Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# -----------------------------
# API DETAILS
# Reads from GitHub Secrets in CI/CD, or uses local defaults
# -----------------------------

import os

API_KEY = os.getenv("API_KEY")

CITY = os.environ.get("CITY", "Colombo")
COUNTRY = os.environ.get("COUNTRY", "LK")

# -----------------------------
# EMAIL DETAILS
# Reads from GitHub Secrets in CI/CD, or uses local defaults
# -----------------------------

SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "deepathangadurai923@gmail.com")
APP_PASSWORD = os.environ.get("APP_PASSWORD", "yhon lsce gnkc iott")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "narmathaashok59@gmail.com")


# -----------------------------
# GET WEATHER DATA
# -----------------------------

url = "https://api.openweathermap.org/data/2.5/weather"

params = {
    "q": f"{CITY},{COUNTRY}",
    "appid": API_KEY,
    "units": "metric"
}

response = requests.get(url, params=params)


if response.status_code == 200:

    data = response.json()

    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]

    # -----------------------------
    # CREATE EMAIL
    # -----------------------------

    subject = "Daily Sri Lanka Weather Update"

    message = f"""
Daily Sri Lanka Weather Update

Location: {CITY}, Sri Lanka

Temperature: {temperature}°C
Weather Condition: {weather}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s

Have a nice day!
"""

    email = MIMEText(message)

    email["Subject"] = subject
    email["From"] = SENDER_EMAIL
    email["To"] = RECEIVER_EMAIL

    # -----------------------------
    # SEND EMAIL
    # -----------------------------

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(SENDER_EMAIL, APP_PASSWORD)

        server.sendmail(
            SENDER_EMAIL,
            RECEIVER_EMAIL,
            email.as_string()
        )

        server.quit()

        print("✅ Weather email sent successfully!")

    except Exception as e:

        print("❌ Email sending failed!")
        print("Error:", e)

else:

    print("❌ Weather data could not be retrieved.")
    print("Status Code:", response.status_code)
    print("Response:", response.text)