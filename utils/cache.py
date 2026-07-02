from __future__ import annotations

import functools
import time
from typing import Any, Callable


_MEMORY_CACHE: dict[tuple[str, str], tuple[float, Any]] = {}


def ttl_cache(ttl: int, namespace: str):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (namespace, repr((args, sorted(kwargs.items()))))
            now = time.time()
            cached = _MEMORY_CACHE.get(key)
            if cached and now - cached[0] <= ttl:
                return cached[1]
            value = func(*args, **kwargs)
            _MEMORY_CACHE[key] = (now, value)
            return value

        wrapper.clear = lambda: clear_cache(namespace)  # type: ignore[attr-defined]
        return wrapper

    return decorator


def clear_cache(namespace: str | None = None) -> None:
    if namespace is None:
        _MEMORY_CACHE.clear()
        return
    for key in list(_MEMORY_CACHE.keys()):
        if key[0] == namespace:
            del _MEMORY_CACHE[key]


def clear_all_caches() -> None:
    clear_cache()
    try:
        import streamlit as st

        st.cache_data.clear()
    except Exception:
        pass


cache_yfinance_prices = lambda func: ttl_cache(300, "yfinance_prices")(func)
cache_yfinance_history = lambda func: ttl_cache(900, "yfinance_history")(func)
cache_fred_data = lambda func: ttl_cache(3600, "fred_data")(func)
cache_binance_price = lambda func: ttl_cache(30, "binance_price")(func)
cache_sector_heat = lambda func: ttl_cache(900, "sector_heat")(func)
cache_market_regime = lambda func: ttl_cache(300, "market_regime")(func)
cache_portfolio_prices = lambda func: ttl_cache(300, "portfolio_prices")(func)
