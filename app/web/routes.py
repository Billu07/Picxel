"""Website pages."""

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.web.templating import templates

router = APIRouter(include_in_schema=False)


@router.get("/", name="home")
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "pages/home.html")
