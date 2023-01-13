import requests
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

############################
# EXAMPLE CODE STARTS HERE #
############################

# Creating a FastAPI app
app = FastAPI()


# CORS (Cross Origin Resource Sharing) needs to be enabled to allow the frontend to access the app
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"],
                   allow_headers=["*"])


# The requirements want root path to return bulbasaur data
@app.get("/")
async def root():
    bulbasaur_data = requests.get("https://pokeapi.co/api/v2/pokemon/bulbasaur").json()
    response_model = {"name": bulbasaur_data["name"], "pokedex_number": bulbasaur_data["id"],
                      "artwork_link": bulbasaur_data["sprites"]["other"]["official-artwork"]["front_default"]}
    return response_model

##########################
# EXAMPLE CODE ENDS HERE #
##########################
