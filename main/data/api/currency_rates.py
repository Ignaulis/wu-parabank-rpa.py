import json
from urllib.request import urlopen

API_URL = "https://api.exchangerate.host/latest?base=USD&symbols=EUR"


def get_usd_to_eur_rate(settings, timeout_seconds: int = 10) -> tuple[float, str]:
    try:
        with urlopen(API_URL, timeout=timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
            rate = float(data["rates"]["EUR"])
            if rate > 0:
                return rate, "api"
    except Exception:
        pass

    return float(settings.usd_to_eur_fallback_rate), "fallback"
