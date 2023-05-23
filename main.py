import requests as req
from datetime import datetime
import os

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = os.environ["SHEETY_ENDPOINT"]

TOKEN = os.environ["TOKEN"]
gender = "male"
height_cm = 173
weight_kg = 60
age = 20

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

body = {
    "query": input("Tell me which exercise you did:"),
    "gender": gender,
    "height_cm": height_cm,
    "weight_kg": weight_kg,
    "age": age
}
today = datetime.now()
today_date = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")
print(time)

res = req.post(url=EXERCISE_ENDPOINT, headers=headers, json=body)
res.raise_for_status()
result = res.json()

headers = {"Authorization": TOKEN}

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    res = req.post(url=SHEETY_ENDPOINT, json=sheet_inputs, headers=headers)
    print(res.raise_for_status())
    print(res.text)
