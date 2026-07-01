from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv

from utils.tradingview import log_alert, validate_webhook_secret


load_dotenv()
app = FastAPI(title="Devin Investment OS Webhooks")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request) -> dict:
    payload = await request.json()
    if not validate_webhook_secret(payload):
        raise HTTPException(status_code=401, detail="unauthorized")
    alert = log_alert(payload)
    return {"ok": True, "action": "logged_only_no_trade", "received_at": alert["received_at"]}
