from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    db_host: str = Field(..., env='DB_HOST')
    db_port: int = Field(..., env='DB_PORT')
    db_user: str = Field(..., env='DB_USER')
    db_password: str = Field(..., env='DB_PASSWORD')
    db_name: str = Field(..., env='DB_NAME')
    
    telegram_bot_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    telegram_chat_id: str = Field(..., env='TELEGRAM_CHAT_ID')
    
    secret_key: str = Field(..., env='SECRET_KEY')
    admin_username: str = Field(..., env='ADMIN_USERNAME')
    admin_password: str = Field(..., env='ADMIN_PASSWORD')
    
    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()