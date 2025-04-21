from fastapi import APIRouter, Request

from aiogram.types import Update


from fastapi.responses import StreamingResponse
import asyncio

router = APIRouter()

subscribers = []


async def notify_update():
    subscribers.append("update")


@router.get("/sse")
async def sse(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            if subscribers:
                message = subscribers.pop(0)
                yield f"data: {message}\n\n"
            await asyncio.sleep(1)

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
