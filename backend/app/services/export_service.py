import csv
from io import StringIO

from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation
from app.models.user import User


def build_recommendations_csv(db: Session, current_user: User) -> str:
    recommendations = (
        db.query(Recommendation)
        .join(Recommendation.report)
        .filter_by(owner_id=current_user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )

    output = StringIO()
    writer = csv.writer(output)

    writer.writerow(
        [
            "Action Type",
            "Search Term",
            "Campaign Name",
            "Reason",
            "Confidence",
            "Status",
        ]
    )

    for recommendation in recommendations:
        writer.writerow(
            [
                recommendation.action_type,
                recommendation.search_term,
                recommendation.campaign_name,
                recommendation.reason,
                recommendation.confidence,
                recommendation.status,
            ]
        )

    return output.getvalue()