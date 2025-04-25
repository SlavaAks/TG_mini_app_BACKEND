from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from services import fetch_csv_data

router = APIRouter()


@router.get("/catalog")
async def get_products() -> JSONResponse:
    try:
        data = await fetch_csv_data()
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
