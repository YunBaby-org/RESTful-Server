import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')