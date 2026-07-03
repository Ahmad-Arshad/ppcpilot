def safe_divide(numerator: float, denominator: float) -> float | None:
    if denominator == 0:
        return None

    return numerator / denominator


def calculate_acos_percent(spend: float, sales: float) -> float | None:
    result = safe_divide(spend, sales)

    if result is None:
        return None

    return round(result * 100, 2)


def calculate_roas(sales: float, spend: float) -> float | None:
    result = safe_divide(sales, spend)

    if result is None:
        return None

    return round(result, 2)


def calculate_ctr_percent(clicks: int, impressions: int) -> float | None:
    result = safe_divide(clicks, impressions)

    if result is None:
        return None

    return round(result * 100, 2)


def calculate_cpc(spend: float, clicks: int) -> float | None:
    result = safe_divide(spend, clicks)

    if result is None:
        return None

    return round(result, 2)


def calculate_conversion_rate_percent(orders: int, clicks: int) -> float | None:
    result = safe_divide(orders, clicks)

    if result is None:
        return None

    return round(result * 100, 2)