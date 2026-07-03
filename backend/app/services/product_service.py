from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate


def create_product(db: Session, current_user: User, payload: ProductCreate) -> Product:
    product = Product(
        owner_id=current_user.id,
        name=payload.name.strip(),
        asin=payload.asin.strip().upper(),
        marketplace=payload.marketplace.strip().upper(),
        selling_price=payload.selling_price,
        profit_margin_percent=payload.profit_margin_percent,
        target_acos_percent=payload.target_acos_percent,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def list_products(db: Session, current_user: User) -> list[Product]:
    return (
        db.query(Product)
        .filter(Product.owner_id == current_user.id)
        .order_by(Product.created_at.desc())
        .all()
    )


def get_product(db: Session, current_user: User, product_id: int) -> Product:
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

    return product


def update_product(
    db: Session,
    current_user: User,
    product_id: int,
    payload: ProductUpdate,
) -> Product:
    product = get_product(db, current_user, product_id)

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product


def delete_product(db: Session, current_user: User, product_id: int) -> None:
    product = get_product(db, current_user, product_id)

    db.delete(product)
    db.commit()