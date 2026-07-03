from datetime import datetime

from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: int
    product_id: int
    file_name: str
    report_type: str
    status: str
    error_message: str | None
    total_rows: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class SearchTermMetricResponse(BaseModel):
    id: int
    campaign_name: str
    ad_group_name: str
    keyword: str | None
    search_term: str
    match_type: str | None
    impressions: int
    clicks: int
    spend: float
    sales: float
    orders: int
    acos_percent: float | None
    roas: float | None
    ctr_percent: float | None
    cpc: float | None
    conversion_rate_percent: float | None

    model_config = {
        "from_attributes": True
    }