from typing import List
from fastapi import APIRouter

from src.main import chatpdf, train_chatpdf
from config.config import PROEJECTS_DIR, logger

chat_router = APIRouter()

@chat_router.post('/chatpdf', tags=['chatpdf'])
def chatpdf_route(project_name: str, query: str):
    projects = [f.name for f in PROEJECTS_DIR.iterdir() if f.is_dir()]
    if project_name not in projects:
        return {"error": f"Project {project_name} does not exist"}
    response = chatpdf(project_name, query)
    return response

@chat_router.post('/train_chatpdf', tags=['chatpdf'])
def train_chatpdf_route(project_name: str):
    projects = [f.name for f in PROEJECTS_DIR.iterdir() if f.is_dir()]
    if project_name not in projects:
        return {"error": f"Project {project_name} does not exist"}
    response = train_chatpdf(project_name)
    return response