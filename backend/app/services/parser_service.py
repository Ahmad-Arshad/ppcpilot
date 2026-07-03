from io import BytesIO

import pandas as pd
from fastapi import HTTPException, UploadFile, status

from app.models.metric import SearchTermMetric
from app.services.metrics_service import (
    calculate_acos_percent,
    calculate_conversion_rate_percent,
    calculate_cpc,
    calculate_ctr_percent,
    calculate_roas,
)

COLUMN_ALIASES = {
    "campaign name": "campaign_name",
    "campaign": "campaign_name",
    "ad group name": "ad_group_name",
    "ad group": "ad_group_name",
    "keyword": "keyword",
    "targeting": "keyword",
    "customer search term": "search_term",
    "search term": "search_term",
    "match type": "match_type",
    "impressions": "impressions",
    "clicks": "clicks",
    "spend": "spend",
    "cost": "spend",
    "7 day total sales": "sales",
    "sales": "sales",
    "total sales": "sales",
    "7 day total orders": "orders",
    "orders": "orders",
    "purchases": "orders",
}

REQUIRED_COLUMNS = {
    "campaign_name",
    "ad_group_name",
    "search_term",
    "impressions",
    "clicks",
    "spend",
    "sales",
    "orders",
}


def normalize_column_name(column: str) -> str:
    cleaned = column.strip().lower().replace("_", " ")
    return COLUMN_ALIASES.get(cleaned, cleaned.replace(" ", "_"))


def clean_money_value(value: object) -> float:
    if pd.isna(value):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    value_as_string = str(value)
    value_as_string = value_as_string.replace("$", "").replace("£", "")
    value_as_string = value_as_string.replace(",", "").strip()

    if not value_as_string:
        return 0.0

    return float(value_as_string)


def clean_int_value(value: object) -> int:
    if pd.isna(value):
        return 0

    if isinstance(value, int):
        return value

    value_as_string = str(value).replace(",", "").strip()

    if not value_as_string:
        return 0

    return int(float(value_as_string))


async def parse_search_term_report(
    report_id: int,
    file: UploadFile,
) -> list[SearchTermMetric]:
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV files are supported.",
        )

    file_bytes = await file.read()

    try:
        dataframe = pd.read_csv(BytesIO(file_bytes))
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read CSV file.",
        ) from exc

    dataframe.columns = [normalize_column_name(column) for column in dataframe.columns]

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)

    if missing_columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required columns: {', '.join(sorted(missing_columns))}",
        )

    metrics: list[SearchTermMetric] = []

    for _, row in dataframe.iterrows():
        campaign_name = str(row.get("campaign_name", "")).strip()
        ad_group_name = str(row.get("ad_group_name", "")).strip()
        search_term = str(row.get("search_term", "")).strip()

        if not campaign_name or not ad_group_name or not search_term:
            continue

        keyword_value = row.get("keyword")
        match_type_value = row.get("match_type")

        impressions = clean_int_value(row.get("impressions"))
        clicks = clean_int_value(row.get("clicks"))
        spend = clean_money_value(row.get("spend"))
        sales = clean_money_value(row.get("sales"))
        orders = clean_int_value(row.get("orders"))

        metric = SearchTermMetric(
            report_id=report_id,
            campaign_name=campaign_name,
            ad_group_name=ad_group_name,
            keyword=None if pd.isna(keyword_value) else str(keyword_value).strip(),
            search_term=search_term,
            match_type=None if pd.isna(match_type_value) else str(match_type_value).strip(),
            impressions=impressions,
            clicks=clicks,
            spend=spend,
            sales=sales,
            orders=orders,
            acos_percent=calculate_acos_percent(spend, sales),
            roas=calculate_roas(sales, spend),
            ctr_percent=calculate_ctr_percent(clicks, impressions),
            cpc=calculate_cpc(spend, clicks),
            conversion_rate_percent=calculate_conversion_rate_percent(orders, clicks),
        )

        metrics.append(metric)

    return metrics