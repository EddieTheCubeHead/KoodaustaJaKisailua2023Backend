from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

application = FastAPI()


origins = ["http://localhost:8000", "https://localhost:8000", "http://127.0.0.1:8000", "https://127.0.0.1:8000"]


application.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                           allow_headers=["*"])
