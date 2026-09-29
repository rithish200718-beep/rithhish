from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# Static files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------------------------
# Request model
# --------------------------------------------------

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# Question Answering
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: TextRequest):

    result = answer_question(payload.text)

    return {
        "result": result
    }


# --------------------------------------------------
# Explain a concept
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: TextRequest):

    result = explain_topic(payload.text)

    return {
        "result": result
    }


# --------------------------------------------------
# Generate quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: TextRequest):

    result = generate_quiz(payload.text)

    return {
        "result": result
    }


# --------------------------------------------------
# Summarize text
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: TextRequest):

    result = summarize_text(payload.text)

    return {
        "result": result
    }


# --------------------------------------------------
# Learning recommendations
# --------------------------------------------------

@app.post("/learn/recommendations")
async def recommendations(payload: TextRequest):

    result = get_learning_recommendations(
        payload.text
    )

    return {
        "result": result
    }


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "EduGenie"
    }