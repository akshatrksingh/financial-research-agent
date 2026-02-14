"""Mock portfolio tool - returns hardcoded user holdings."""

def get_portfolio(user_id: str = "demo") -> dict:
    """Get user's portfolio holdings."""
    return {
        "user_id": user_id,
        "cash": 5000.00,
        "holdings": [
            {"ticker": "AAPL", "shares": 10, "avg_cost": 150.00},
            {"ticker": "NVDA", "shares": 5, "avg_cost": 400.00},
        ],
        "total_value": 9500.00
    }

if __name__ == "__main__":
    print(get_portfolio())