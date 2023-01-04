import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

application = FastAPI()
API_URL = os.getenv("POKEAPI_URL", "https://pokeapi.co/api/v2")


application.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                           allow_headers=["*"])
