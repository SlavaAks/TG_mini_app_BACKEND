from fastapi import APIRouter, Request

from aiogram.types import Update
from datetime import datetime


from fastapi.responses import StreamingResponse
import asyncio
from typing import Optional

router = APIRouter()

subscriber_queues = []


async def notify_all(message: str):
    for queue in subscriber_queues:
        await queue.put(message)


# Переменная для хранения последнего времени обновления
last_updated: Optional[datetime] = None

async def set_last_updated():
    global last_updated
    last_updated = datetime.utcnow()
    print(f"✅ Last updated set to {last_updated.isoformat()}")

async def get_last_updated() -> Optional[datetime]:
    return last_updated

@router.get("/last-updated")
async def last_updated_endpoint():
    """
    Эндпоинт для получения времени последнего обновления данных
    """
    last_updated = get_last_updated()
    if last_updated is None:
        return {"last_updated": None}
    return {"last_updated": last_updated.isoformat()}



@router.get("/sse/")
async def sse(request: Request):
    queue = asyncio.Queue()
    subscriber_queues.append(queue)

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break

                try:
                    # Получаем сообщение с таймаутом (пинг каждые 15 сек)
                    message = await asyncio.wait_for(queue.get(), timeout=15)
                    yield f"data: {message}\n\n"
                except asyncio.TimeoutError:
                    # Пинг для удержания соединения
                    yield ": ping\n\n"

        finally:
            subscriber_queues.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/webhook")
async def webhook(request: Request) -> None:
    try:
        bot = request.app.state.bot
        dp = request.app.state.dp

        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)

    except Exception as e:
        raise e

