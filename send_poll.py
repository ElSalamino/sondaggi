import os
import json
import random
import datetime as dt
from zoneinfo import ZoneInfo

import requests

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]  # es: "@nomecanale"

TZ = ZoneInfo("Europe/Rome")
START_DATE = dt.date(2026, 1, 1)  # puoi cambiarla: è la "domanda 1"

# ============================
# LOAD DOMANDE
# ============================

with open("sondaggi_365.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if not isinstance(data, dict) or not data:
    raise ValueError("sondaggi_365.json deve essere un dict non vuoto: {'Domanda?': ['A','B',...]}")

# Ordine stabile delle domande
questions = sorted(data.items(), key=lambda kv: kv[0])

today = dt.datetime.now(TZ).date()
idx = (today - START_DATE).days % len(questions)

question, opts = questions[idx]

# ============================
# SEND POLL
# ============================

poll_payload = {
    "chat_id": CHAT_ID,
    "question": question,
    "options": [{"text": o} for o in opts],
    "is_anonymous": True,
    "type": "regular",
}

poll_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPoll"

r = requests.post(poll_url, json=poll_payload, timeout=20)
print("POLL:", r.status_code, r.text)
r.raise_for_status()

# ============================
# 15% CHANCE SEND CATCH
# ============================

if random.random() < 0.15:

    with open("catch.json", "r", encoding="utf-8") as f:
        catch_data = json.load(f)

    catches = catch_data.get("catchphrases")

    if not catches:
        raise ValueError("catch.json deve contenere {'catchphrases': [...]}")

    msg = random.choice(catches)

    msg_payload = {
        "chat_id": CHAT_ID,
        "text": msg,
    }

    msg_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    r2 = requests.post(msg_url, json=msg_payload, timeout=20)
    print("CATCH:", r2.status_code, r2.text)
    r2.raise_for_status()
