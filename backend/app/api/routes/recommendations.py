from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.database import get_db
from app.models.recommendation import Recommendation
from app.models.user import User
from app.schemas.recommendation import RecommendationResponse, RecommendationStatusUpdate

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=list[RecommendationResponse])
def list_recommendations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Recommendation)
        .join(Recommendation.report)
        .filter_by(owner_id=current_user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )


@router.patch("/{recommendation_id}", response_model=RecommendationResponse)
def update_recommendation_status(
    recommendation_id: int,
    payload: RecommendationStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    recommendation = (
        db.query(Recommendation)
        .join(Recommendation.report)
        .filter(Recommendation.id == recommendation_id)
        .filter_by(owner_id=current_user.id)
        .first()
    )

    if not recommendation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recommendation not found.",
        )

    allowed_statuses = {"PENDING", "APPROVED", "REJECTED", "EXPORTED"}

    if payload.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid status.",
        )

    recommendation.status = payload.status
    db.commit()
    db.refresh(recommendation)

    return recommendation