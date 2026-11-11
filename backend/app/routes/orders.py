
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_current_user
from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderResponse, OrderDetailResponse


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# Place Order
@router.post("/", response_model=OrderResponse)
def place_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cart_items = db.query(CartItem).filter(
        CartItem.user_id == current_user.id
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=400,
            detail="Cart is empty"
        )

    total_amount = Decimal("0.00")
    order_products = []

    for item in cart_items:
        product = db.query(Product).filter(
            Product.id == item.product_id,
            Product.is_active == True
        ).first()

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        if item.quantity > product.stock:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        price = Decimal(str(product.price))
        total_amount += price * item.quantity

        order_products.append((item, product, price))

    try:
        new_order = Order(
            user_id=current_user.id,
            total_amount=total_amount,
            status="Pending"
        )

        db.add(new_order)
        db.flush()

        for item, product, price in order_products:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=price
            )

            db.add(order_item)
            product.stock -= item.quantity
            db.delete(item)

        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception:
        db.rollback()
        raise


# Get My Orders
@router.get("/", response_model=list[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(
        Order.created_at.desc()
    ).all()

    return orders


# Get Order Details
@router.get("/{order_id}", response_model=OrderDetailResponse)
def get_order_details(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order_items = db.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).all()

    return {
        "id": order.id,
        "user_id": order.user_id,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at,
        "items": order_items
    }


# Cancel Order
@router.patch("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )

    try:
        # Restore Product Stock
        order_items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        for item in order_items:
            product = db.query(Product).filter(
                Product.id == item.product_id
            ).first()

            if product:
                product.stock += item.quantity

        # Update Order Status
        order.status = "Cancelled"

        db.commit()
        db.refresh(order)

        return {
            "message": "Order cancelled successfully",
            "order_id": order.id,
            "status": order.status
        }

    except Exception:
        db.rollback()
        raise
