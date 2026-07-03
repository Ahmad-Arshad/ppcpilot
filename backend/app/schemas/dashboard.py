from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_reports: int
    total_spend: float
    total_sales: float
    total_orders: int
    overall_acos_percent: float | None
    overall_roas: float | None
    wasted_spend: float
    pending_recommendations: int