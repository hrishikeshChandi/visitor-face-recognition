import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("HOST")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")
IMAGES_FOLDER = os.getenv("IMAGES_FOLDER")
UPLOADS_FOLDER = os.getenv("UPLOADS_FOLDER")
INDEX_PATH = os.getenv("INDEX_PATH")
EMBEDDINGS_PATH = os.getenv("EMBEDDINGS_PATH")