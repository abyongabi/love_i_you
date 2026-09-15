from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()

@dataclass
class AppConfig:
    db_url: str = os.environ["DB_URL"]
    jwt_secret: str = os.environ["JWT_SECRET"]


app_config = AppConfig()
