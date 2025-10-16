from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""

    # 基本配置
    PROJECT_NAME: str = "金融分析系统API"
    VERSION: str = "2.0.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS配置
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    # 数据库配置
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost:3306/financial_analysis"

    # AKShare配置
    AKSHARE_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
