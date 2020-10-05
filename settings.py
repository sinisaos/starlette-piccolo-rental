from starlette.config import Config
from starlette.templating import Jinja2Templates

# Configuration from environment variables or '.env' file.
config = Config(".env")
DB_NAME = config("DB_NAME")
DB_USER = config("DB_USER")
DB_PASSWORD = config("DB_PASSWORD")
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
SECRET_KEY = config("SECRET_KEY")
templates = Jinja2Templates(directory="templates")
BASE_HOST = "http://localhost:8000"
