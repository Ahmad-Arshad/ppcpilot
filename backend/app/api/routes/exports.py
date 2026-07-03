from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.services.export_service import build_recommendations_csv

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.get("/recommendations.csv")
def export_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    csv_content = build_recommendations_csv(db, current_user)

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=ppcpilot_recommendations.csv"
        },
    )