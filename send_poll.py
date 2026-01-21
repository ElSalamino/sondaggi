import os
import json
import datetime as dt
from zoneinfo import ZoneInfo

import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]  # es: "@nomecanale"

TZ = ZoneInfo("Europe/Rome")
START_DATE = dt.date(2026, 1, 1)  # puoi cambiarla: è la "domanda 1"

with open("sondaggi_365.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if not isinstance(data, dict) or not data:
    raise ValueError("sondaggi_365.json deve essere un dict non vuoto: {'Domanda?': ['A','B',...]}")

# Ordine stabile delle domande (in base al testo)
questions = sorted(data.items(), key=lambda kv: kv[0])

today = dt.datetime.now(TZ).date()
idx = (today - START_DATE).days % len(questions)

question, opts = questions[idx]

payload = {
    "chat_id": CHAT_ID,
    "question": question,
    "options": [{"text": o} for o in opts],  # formato InputPollOption
    "is_anonymous": True,
    "type": "regular",
}

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"
r = requests.post(url, json=payload, timeout=20)
print(r.status_code, r.text)
r.raise_for_status()
