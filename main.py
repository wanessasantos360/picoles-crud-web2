<<<<<<< HEAD
from fastapi import FastAPI
=======
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi import status
>>>>>>> ffgit29a13c58ff5b95645c66d00f5e6cf724eb95ef
from api.api import api_router


app = FastAPI()

app.include_router(api_router)