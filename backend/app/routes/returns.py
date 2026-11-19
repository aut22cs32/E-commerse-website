from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.models.order import Order, OrderItem
from app.models.return_request import ReturnRequest
from app.models.user import User
from app.schemas.return_request import ReturnRequestCreate


router = APIRouter(prefix="/returns", tags=["Returns"])


def return_data(request, order_item):
    return {
        "id": request.id,
        "order_id": request.order_id,
        "order_item_id": request.order_item_id,
        "product_id": order_item.product_id,
        "product_name": order_item.product.name,
        "reason": request.reason,
        "status": request.status,
        "created_at": request.created_at,
    }


@router.get("/")
def get_my_return_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = db.query(ReturnRequest, OrderItem).join(
        OrderItem, OrderItem.id == ReturnRequest.order_item_id
    ).filter(ReturnRequest.user_id == current_user.id).order_by(
        ReturnRequest.created_at.desc()
    ).all()
    return [return_data(request, item) for request, item in rows]


@router.post("/orders/{order_id}/items/{order_item_id}")
def request_return(
    order_id: int,
    order_item_id: int,
    data: ReturnRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id,
    ).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    order_item = db.query(OrderItem).filter(
        OrderItem.id == order_item_id,
        OrderItem.order_id == order_id,
    ).first()
    if order_item is None:
        raise HTTPException(status_code=404, detail="Order item not found")

    existing = db.query(ReturnRequest).filter(
        ReturnRequest.order_item_id == order_item_id
    ).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="A return request already exists for this item")

    request = ReturnRequest(
        user_id=current_user.id,
        order_id=order_id,
        order_item_id=order_item_id,
        reason=data.reason.strip(),
    )
    db.add(request)
    db.commit()
    db.refresh(request)
    return return_data(request, order_item)
