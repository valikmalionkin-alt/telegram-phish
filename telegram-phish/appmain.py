from fastapi import FastAPI
from app.routers import auth, admin

app = FastAPI(title="Telegram Phish (Educational)")

app.include_router(auth.router)
app.include_router(admin.router)

@app.on_event("startup")
async def startup():
    # Проверим подключение к БД и создадим админа, если нет
    from app.services.db_service import AsyncSessionLocal
    from app.models.models import AdminUser
    from app.core.security import get_password_hash
    from app.core.config import settings
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as session:
        # Создаём админа из .env, если его нет
        result = await session.execute(select(AdminUser).where(AdminUser.username == settings.admin_username))
        admin = result.scalar_one_or_none()
        if not admin:
            admin = AdminUser(
                username=settings.admin_username,
                hashed_password=get_password_hash(settings.admin_password)
            )
            session.add(admin)
            await session.commit()