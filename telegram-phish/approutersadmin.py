from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.db_service import get_db
from app.models.models import UserCred, AdminUser
from app.core.security import verify_password
from app.core.config import settings
import secrets

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")
security = HTTPBasic()

async def authenticate_admin(credentials: HTTPBasicCredentials = Depends(security)):
    """Проверяет логин/пароль для доступа к админке."""
    # В реальном проекте проверял бы по БД, но для простоты используем настройки
    correct_username = secrets.compare_digest(credentials.username, settings.admin_username)
    correct_password = secrets.compare_digest(credentials.password, settings.admin_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@router.get("/", response_class=HTMLResponse)
async def admin_panel(
    request: Request,
    db: AsyncSession = Depends(get_db),
    _: str = Depends(authenticate_admin)
):
    """Отображает все собранные данные."""
    result = await db.execute(select(UserCred).order_by(UserCred.created_at.desc()))
    creds = result.scalars().all()
    return templates.TemplateResponse("admin.html", {"request": request, "creds": creds})