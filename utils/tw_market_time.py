from __future__ import annotations

from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo


TAIPEI_TZ = ZoneInfo("Asia/Taipei")
MARKET_OPEN = time(9, 0)
MARKET_CLOSE = time(13, 30)


def get_taiwan_now() -> datetime:
    return datetime.now(TAIPEI_TZ)


def is_tw_market_open(now: datetime | None = None) -> bool:
    current = now.astimezone(TAIPEI_TZ) if now else get_taiwan_now()
    return current.weekday() < 5 and MARKET_OPEN <= current.time() <= MARKET_CLOSE


def get_tw_market_session_label(now: datetime | None = None) -> str:
    current = now.astimezone(TAIPEI_TZ) if now else get_taiwan_now()
    if current.weekday() >= 5:
        return "Closed"
    if current.time() < MARKET_OPEN:
        return "Pre-market"
    if current.time() <= MARKET_CLOSE:
        return "Open"
    return "Post-market"


def get_tw_next_session_hint(now: datetime | None = None) -> str:
    current = now.astimezone(TAIPEI_TZ) if now else get_taiwan_now()
    next_day = current
    if current.weekday() < 5 and current.time() < MARKET_OPEN:
        next_open = current.replace(hour=9, minute=0, second=0, microsecond=0)
    else:
        next_day = current + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        next_open = next_day.replace(hour=9, minute=0, second=0, microsecond=0)
    return f"Next regular TWSE reference session: {next_open.strftime('%Y-%m-%d %H:%M')} Taipei time"
