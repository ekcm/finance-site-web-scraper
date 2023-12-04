from fastapi import FastAPI
import os
from json import JSONDecodeError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument('--start-maximized')


@app.get("/webscrape/{company}")
async def webscrape_company_name(company: str):

  return company

capitalIQUrl = "https://secure.signin.spglobal.com/sso/saml2/0oa1n9y64jc36qEBE1d8/app/spglobaliam_sp_1/exk1mregn1oWwP2NB1d8/sso/saml?RelayState=https%3A%2F%2Fwww.capitaliq.com%2FCIQDotNet%2Fsaml-sso.aspx"
  
# driver = webdriver.Chrome()
# driver.maximize_window()
# driver.get(capitalIQUrl)
# time.sleep(5)
# driver.close()

url = 'http://libproxy.smu.edu.sg/login?url=https://orbis4.bvdinfo.com/ip'
orbis = webdriver.Chrome(options=chrome_options)
orbis.get(url)

un_locator = (By.ID, 'userNameInput')
un = WebDriverWait(orbis, 5).until(EC.presence_of_element_located(un_locator))
un.send_keys(username)
pwd = orbis.find_element(By.ID, 'passwordInput')
pwd.send_keys(password)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("webscraper:app", host='127.0.0.1', port=5000, reload=True)