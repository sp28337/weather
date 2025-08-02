import os

from dotenv import load_dotenv
from uvicorn_worker import UvicornWorker

bind = "0.0.0.0:8000"
workers = 4
worker_class = UvicornWorker

load_dotenv()
env = os.path.join(os.getcwd(), ".env")
if os.path.exists(env):
    load_dotenv(env)
