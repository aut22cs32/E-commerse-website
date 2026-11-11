
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Create Product
@router.post("/", response_model=ProductResponse)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = Product(**product_data.model_dump())

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# Get All Products
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()


# Get Product By ID
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id,
        Product.is_active == True
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


# Update Product
@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    update_data = product_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product



# Delete Product (Soft Delete)
@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.is_active = False

    db.commit()

    return {
        "message": "Product deleted successfully"
    }

