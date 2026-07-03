from datetime import datetime

from pydantic import BaseModel


class RecommendationResponse(BaseModel):
    id: int
    report_id: int
    action_type: str
    search_term: str
    campaign_name: str
    reason: str
    confidence: float
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class RecommendationStatusUpdate(BaseModel):
    status: str