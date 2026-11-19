from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.product import Product
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreate


router = APIRouter(prefix="/products", tags=["Reviews"])


def review_data(review, name):
    return {
        "id": review.id,
        "product_id": review.product_id,
        "user_id": review.user_id,
        "name": name,
        "stars": review.stars,
        "review": review.review,
        "created_at": review.created_at,
    }


@router.get("/{product_id}/reviews")
def get_product_reviews(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active.is_(True)).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    rows = db.query(Review, User.name).join(User, User.id == Review.user_id).filter(
        Review.product_id == product_id
    ).order_by(Review.created_at.desc()).all()
    reviews = [review_data(review, name) for review, name in rows]
    average = round(sum(item["stars"] for item in reviews) / len(reviews), 1) if reviews else None
    return {"reviews": reviews, "average_rating": average, "count": len(reviews)}


@router.post("/{product_id}/reviews")
def save_product_review(
    product_id: int,
    review_data_input: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active.is_(True)).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    review = db.query(Review).filter(
        Review.user_id == current_user.id,
        Review.product_id == product_id,
    ).first()
    if review is None:
        review = Review(user_id=current_user.id, product_id=product_id)
        db.add(review)

    review.stars = review_data_input.stars
    review.review = review_data_input.review.strip()
    db.commit()
    db.refresh(review)
    return review_data(review, current_user.name)
