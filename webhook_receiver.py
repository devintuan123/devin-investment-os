from json import JSONDecodeError

from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv

from utils.tradingview import log_alert, validate_webhook_secret


load_dotenv()
app = FastAPI(title="Devin Investment OS Webhooks")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.head("/health")
def health_head() -> dict:
    return {"status": "ok"}


@app.post("/tradingview-webhook")
async def tradingview_webhook(request: Request) -> dict:
    try:
        payload = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="invalid json")
    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="json body must be an object")
    if not validate_webhook_secret(payload):
        raise HTTPException(status_code=401, detail="unauthorized")
    alert = log_alert(payload)
    return {"ok": True, "action": "logged_only_no_trade", "received_at": alert["received_at"]}
