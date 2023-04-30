from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from config.config import PROEJECTS_DIR, logger
from app.config.database import engine, Base
from app.middlewares.error_handler import ErrorHandler
from app.routers.chatpdf import chat_router
from app.routers.ocr import ocr_router

app = FastAPI()
app.title = "ChatPDF with FastAPI"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(chat_router)
app.include_router(ocr_router)

Base.metadata.create_all(bind=engine)

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>ChatPDF Server</h1>')

@app.get('/projects', tags=['home'])
def get_projects():
    projects = [f.name for f in PROEJECTS_DIR.iterdir() if f.is_dir()]
    return JSONResponse(status_code=200, content=jsonable_encoder(projects))

@app.post("/create", tags=['home'])
def create_project(project_name: str):
    return "Not implemented yet"

@app.post("/loadpdf", tags=['home'])
def load_pdf(project_name: str):
    return "Not implemented yet"