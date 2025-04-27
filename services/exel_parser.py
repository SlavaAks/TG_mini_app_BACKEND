import os
from pathlib import Path

from fastapi import FastAPI
import pandas as pd
import requests


from config_reader import config

CSV_FILE_PATH = Path(__file__).resolve().parent / 'product_list.csv'

app = FastAPI()

# --- Настройки ---
CSV_URL = f"https://docs.google.com/spreadsheets/d/{config.SPREADSHEET_ID.get_secret_value()}/export?format=csv"


async def download_csv_file():
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
        with open(CSV_FILE_PATH, 'w',) as f:
            f.write(response.content.decode('utf-8'))

    except Exception as e:
        raise RuntimeError(f"Ошибка при скачивании файла: {e}")


async def fetch_csv_data():
    """
    Получает данные из Google Sheets (CSV) и возвращает список словарей.
    """
    try:
        if not os.path.exists(CSV_FILE_PATH):
            await download_csv_file()
        df = pd.read_csv(CSV_FILE_PATH, header=None)
        df = df.replace({pd.NA: None, float("nan"): None})
        data = df.to_dict(orient="records")

        return data

    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки или парсинга CSV: {str(e)}")



