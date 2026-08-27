
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://sidra_fabrics:sidra_fabrics@localhost:5432/sidra_fabrics")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
