from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Optional

from config_reader import config

router = APIRouter()


# Модели данных
class CartItem(BaseModel):
    title: str
    articul: str
    size: str
    price: float


class Order(BaseModel):
    fullName: str
    phone: str
    email: str
    size: str
    deliveryMethod: str
    address: str
    discount: Optional[str] = ""
    cart: List[CartItem]
    timestamp: str
    total: float
    zip: Optional[str] = ""


@router.post("/order")
async def process_order(order: Order, request: Request):
    bot = request.app.state.bot
    channel_id = config.CHANEL_ID.get_secret_value()

    lines = [
        "🛍 <b>Новый заказ</b>",
        f"<b>ФИО:</b> {order.fullName}",
        f"<b>Телефон:</b> {order.phone}",
        f"<b>Email:</b> {order.email}",
        f"<b>Длина стопы:</b> {order.size} см",
        f"<b>Доставка:</b> {order.deliveryMethod}",
        f"<b>Адрес:</b> {order.address}",
    ]

    if order.zip:
        lines.append(f"<b>Индекс:</b> {order.zip}")
    if order.discount:
        lines.append(f"<b>Скидка:</b> {order.discount}")

    lines.append("\n<b>🧾 Товары:</b>")
    for item in order.cart:
        lines.append(
            f"• {item.title} ({item.articul})\n  Размер: {item.size} — {item.price} BYN"
        )

    lines.append(f"\n<b>💰 Итого:</b> {order.total} BYN")
    lines.append(f"<i>🕒 Время: {order.timestamp}</i>")

    text = "\n".join(lines)

    # Отправка сообщения
    await bot.send_message(chat_id=channel_id, text=text, parse_mode="HTML")

    return {"status": "ok", "message": "Order sent to Telegram"}
