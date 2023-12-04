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

import re
from bs4 import BeautifulSoup

load_dotenv()
email = os.getenv("email")
password = os.getenv("password")
# username = "elijah.khor.2021@scis.smu.edu.sg"
# password = "AyabeKyoto1!"

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

  url = 'http://libproxy.smu.edu.sg/login?url=https://orbis4.bvdinfo.com/ip'
  driver = webdriver.Chrome(options=chrome_options)
  driver.maximize_window()
  driver.get(url)
  wait = WebDriverWait(driver, 10)

  time.sleep(1)
  username_field = driver.find_element(By.ID, 'userNameInput')
  username_field.send_keys(email)
  password_field = driver.find_element(By.ID, 'passwordInput')
  password_field.send_keys(password)
  password_field.send_keys(Keys.RETURN)
  time.sleep(5)

  try:
    # inputs company name into search bar
    company_input_locator = (By.ID, 'search')
    company_input = wait.until(EC.presence_of_element_located(company_input_locator))
    company_input.send_keys(company)

    search_results = (By.CLASS_NAME, 'suggestions')
    suggestions = wait.until(EC.presence_of_element_located(search_results))


    first_result = (By.CSS_SELECTOR, 'a[role="link"]')
    first = wait.until(EC.presence_of_element_located(first_result))
    first.click()

    time.sleep(10)
    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')
    record_name = soup.find('div', class_='recordName')
    extracted_text = record_name.text
    print(extracted_text)

    trimmed_extracted_text = extracted_text.strip()
    trimmed_extracted_text = re.sub(r'\n', '', trimmed_extracted_text)
    return trimmed_extracted_text

  
  except:
     return "not able to find result"


  


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("webscraper:app", host='127.0.0.1', port=5000, reload=True)