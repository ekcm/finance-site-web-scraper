from fastapi import FastAPI
import os
from json import JSONDecodeError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("username")
password = os.getenv("password")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/webscrape/{company}")
async def webscrape_company_name(company: str):
    return company
    


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("webscraper:app", host='127.0.0.1', port=5000, reload=True)