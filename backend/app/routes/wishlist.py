from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.product import Product
from app.models.user import User
from app.models.wishlist import WishlistItem
from app.schemas.wishlist import WishlistItemCreate, WishlistItemResponse


router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("/", response_model=list[WishlistItemResponse])
def get_wishlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(WishlistItem).filter(WishlistItem.user_id == current_user.id).all()


@router.post("/", response_model=WishlistItemResponse)
def add_to_wishlist(
    data: WishlistItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    product = db.query(Product).filter(Product.id == data.product_id, Product.is_active.is_(True)).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    item = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.product_id == product.id,
    ).first()
    if item is None:
        item = WishlistItem(user_id=current_user.id, product_id=product.id, product=product)
        db.add(item)
        db.commit()
        db.refresh(item)
    return item


@router.delete("/{product_id}")
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.product_id == product_id,
    ).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    db.delete(item)
    db.commit()
    return {"message": "Product removed from wishlist"}
