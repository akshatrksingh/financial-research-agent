import requests
from typing import Dict, Any

def get_stock_data(ticker: str) -> Dict[str, Any]:
    # Stooq format often wants AAPL.US for US stocks
    sym = ticker.upper()
    if "." not in sym:
        sym = f"{sym}.US"

    url = f"https://stooq.com/q/l/?s={sym}&f=sd2t2ohlcv&h&e=csv"

    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        lines = r.text.strip().splitlines()
        if len(lines) < 2:
            return {"error": "No data returned", "ticker": ticker.upper()}

        header = lines[0].split(",")
        row = lines[1].split(",")
        d = dict(zip(header, row))

        if d.get("Close") in (None, "", "N/A"):
            return {"error": "Invalid ticker or no data available", "ticker": ticker.upper()}

        def f(x):
            try:
                return float(x)
            except Exception:
                return None

        def i(x):
            try:
                return int(float(x))
            except Exception:
                return None

        return {
            "ticker": ticker.upper(),
            "price": f(d.get("Close")),
            "day_high": f(d.get("High")),
            "day_low": f(d.get("Low")),
            "open": f(d.get("Open")),
            "volume": i(d.get("Volume")),
            "date": d.get("Date"),
            "time": d.get("Time"),
            "source": "stooq",
        }
    except Exception as e:
        return {"error": str(e), "ticker": ticker.upper()}


if __name__ == "__main__":
    data = get_stock_data("AAPL")
    print(data)