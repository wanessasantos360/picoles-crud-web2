from fastapi import FastAPI, APIRouter, HTTPException
from fastapi import status
from api.api import api_router


app = FastAPI()

app.include_router(api_router)