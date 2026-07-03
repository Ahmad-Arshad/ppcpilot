from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.report import ReportStatus, UploadedReport
from app.models.user import User
from app.services.parser_service import parse_search_term_report
from app.services.recommendation_engine import build_recommendations


async def upload_and_process_report(
    db: Session,
    current_user: User,
    product_id: int,
    file: UploadFile,
) -> UploadedReport:
    product = (
        db.query(Product)
        .filter(Product.id == product_id, Product.owner_id == current_user.id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    report = UploadedReport(
        owner_id=current_user.id,
        product_id=product.id,
        file_name=file.filename or "uploaded_report.csv",
        status=ReportStatus.UPLOADED.value,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    try:
        metrics = await parse_search_term_report(report.id, file)

        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid rows found in CSV.",
            )

        db.add_all(metrics)
        db.commit()

        for metric in metrics:
            db.refresh(metric)

        recommendations = build_recommendations(product, metrics)

        if recommendations:
            db.add_all(recommendations)

        report.status = ReportStatus.COMPLETED.value
        report.total_rows = len(metrics)
        db.commit()
        db.refresh(report)

        return report

    except Exception as exc:
        report.status = ReportStatus.FAILED.value
        report.error_message = str(exc)
        db.commit()

        if isinstance(exc, HTTPException):
            raise exc

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Report processing failed.",
        ) from exc


def list_reports(db: Session, current_user: User) -> list[UploadedReport]:
    return (
        db.query(UploadedReport)
        .filter(UploadedReport.owner_id == current_user.id)
        .order_by(UploadedReport.created_at.desc())
        .all()
    )