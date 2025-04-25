from fastapi import APIRouter, Request

from aiogram.types import Update


from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter(prefix="/api")

subscriber_queues = []


async def notify_all(message: str):
    for queue in subscriber_queues:
        await queue.put(message)


@router.get("/sse")
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

