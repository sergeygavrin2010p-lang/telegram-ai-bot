
import os
from fastapi import FastAPI
from openai import OpenAI
import requests

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/webhook")
async def webhook(update: dict):
    try:
        message = update.get("message", {})
        chat_id = message.get("chat", {}).get("id")
        text = message.get("text", "")

        if chat_id and text:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=text
            )
            answer = response.output_text

            requests.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": answer},
                timeout=30
            )

        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
