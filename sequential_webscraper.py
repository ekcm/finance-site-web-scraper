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
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

def start_driver():
  driver = webdriver.Chrome(options=chrome_options)
  driver.maximize_window()
  return driver

def webscrape_orbis(company):
  url = 'http://libproxy.smu.edu.sg/login?url=https://orbis4.bvdinfo.com/ip'
  driver = start_driver()
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
    print("entering Orbis")
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

    orbis_extracted_info = {}

    soup = BeautifulSoup(html, 'html.parser')
    record_name = soup.find('div', class_='recordName')
    extracted_text = record_name.text

    trimmed_extracted_text = extracted_text.strip()
    trimmed_extracted_text = re.sub(r'\n', '', trimmed_extracted_text)

    label_dict = {}

    datatable = soup.find('table', {'class':'FinDataTable'})
    if datatable is None:
      pass
    else:
      print("datatable exists")

      label_tags = soup.find_all("td", class_="finSimpleTD finSimpleLabel")

      # Loop through each label tag and extract its text and next sibling value
      for label_tag in label_tags:
          # Extract the text content of the label tag
          label_text = label_tag.find("div").text.strip()

          # Extract the next sibling "td" tag which contains the financial value
          value_tag = label_tag.find_next_sibling("td")

          # Extract the text content of the value tag
          value_text = value_tag.text.strip()


          label_dict[label_text] = value_text
      orbis_extracted_info[trimmed_extracted_text] = label_dict

      return orbis_extracted_info

  except Exception as e:
     print(f"error message: {e}")
     return {"message": "failed"}

def webscrape_capitalIQ(company):
  # this link will bring you to the capitalIQ home page first to log in
  url = 'https://www.capitaliq.com/ciqdotnet/login-okta.aspx?code=6'
  driver = start_driver()
  driver.get(url)
  wait = WebDriverWait(driver, 10)
  
  time.sleep(1)
  capitalIQ_username_field = (By.ID, "input28")
  element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located(capitalIQ_username_field)
  )

  # keys in username details to redirect to SMU's page
  username_field = driver.find_element(By.ID, "input28")
  username_field.send_keys(email)

  next_button = driver.find_element(By.CLASS_NAME, "button-primary")
  next_button.click()

  # redirected to SMU login page
  element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.ID, "userNameInput"))
  )
  username_field = driver.find_element(By.ID, 'userNameInput')
  username_field.send_keys(email)
  password_field = driver.find_element(By.ID, 'passwordInput')
  password_field.send_keys(password)
  password_field.send_keys(Keys.RETURN)

  time.sleep(5)
  WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
  )
  print("entering CapitalIQ")

  # search for company
  try:
    print("entering try block")
    WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.ID, "SearchTopBar"))
    )
    company_search_bar = driver.find_element(By.ID, "SearchTopBar")
    company_search_bar.send_keys(company)
    time.sleep(2)
    company_search_bar.send_keys(Keys.RETURN)
    
    # search page
    print("entering search page from search bar")
    WebDriverWait(driver, 30).until(
      EC.presence_of_element_located((By.ID, "SR0"))
    )

    driver.find_element(By.CSS_SELECTOR, "td.NameCell a").click()

    time.sleep(5)
    # capitalIQ company financials page
    print("at company financials page")
    WebDriverWait(driver, 30).until(
      EC.presence_of_element_located((By.CLASS_NAME, "cTblListBody"))
    )
    print("company financials page fully loaded")

    company_name_element = driver.find_element(By.ID, "CompanyHeaderInfo")
    company_name_html = company_name_element.get_attribute("outerHTML")
    soup = BeautifulSoup(company_name_html, 'html.parser')

    company_span = soup.find('div', {'id': 'CompanyHeaderInfo'}).find('span', {'class':'cPageTitle_subHeader'})
    company_name = company_span.find_previous('span').text.strip()

    table_elements = driver.find_elements(By.CLASS_NAME, "cTblListBody")

    capitalIQ_data = {}
    for i in range(len(table_elements)):

      if i == 7 or i == 8:
        stock_quote_html = table_elements[i].get_attribute("outerHTML")
        soup = BeautifulSoup(stock_quote_html, 'html.parser')

        cells = soup.find_all(['td', 'th'])

        for i in range(0, len(cells), 2):
          key = cells[i].text.strip()
          value = cells[i+1].text.strip()
          if key == "" or value == "":
            pass
          else:
            capitalIQ_data[key] = value

    capitalIQ_extracted_info = {}
    capitalIQ_extracted_info[company_name] = capitalIQ_data

    return capitalIQ_extracted_info

  except:
    return {"message":"failed"}

@app.get("/api/webscrape/{company}")
def webscrape_company_name(company: str):
  start_time = time.time()

  webscraped_data = {}
  orbis = webscrape_orbis(company)
  webscraped_data["orbis"] = orbis
  capitalIQ = webscrape_capitalIQ(company)
  webscraped_data["capitalIQ"] = capitalIQ
  
  end_time = time.time()
  elapsed_time = end_time - start_time
  print(f"Elapsed time: {elapsed_time}")

  return webscraped_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("sequential_webscraper:app", host='127.0.0.1', port=5000, reload=True)