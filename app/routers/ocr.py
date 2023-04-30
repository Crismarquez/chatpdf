from typing import List
from fastapi import APIRouter
from fastapi.responses import  JSONResponse
from fastapi.encoders import jsonable_encoder

from config.config import PROEJECTS_DIR, logger

ocr_router = APIRouter()

@ocr_router.post('/ocr_engineering', tags=['ocr'])
def process_pdf(project_name: str):
    return "Not implemented yet"
