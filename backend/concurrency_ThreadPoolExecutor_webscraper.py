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
from concurrent.futures import ThreadPoolExecutor


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
  orbis_start_time = time.time()
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

      orbis_end_time = time.time()
      orbis_elapsed_time = orbis_end_time - orbis_start_time
      print(f"orbis webscraper took {orbis_elapsed_time}")

      return orbis_extracted_info

  except Exception as e:
    orbis_end_time = time.time()
    orbis_elapsed_time = orbis_end_time - orbis_start_time
    print(f"orbis webscraper took {orbis_elapsed_time}")
  
    print(f"error message: {e}")
    return {"message": "failed"}

def webscrape_capitalIQ(company):
  capitalIQ_start_time = time.time()
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

    capitalIQ_end_time = time.time()
    capitalIQ_elapsed_time = capitalIQ_end_time - capitalIQ_start_time
    print(f"capitalIQ elapsed time: {capitalIQ_elapsed_time}")

    return capitalIQ_extracted_info

  except:
    return {"message":"failed"}
    
@app.get("/api/webscrape/{company}")
def webscrape_company_name(company: str):

  webscraped_data = {"orbis":{"APPLE INC.":{"Operating revenue (Turnover)":"383,285,000","P/L before tax":"113,736,000","P/L for period [=Net income]":"96,995,000","Cash flow [Net Income before D&A]":"108,514,000","Total assets":"352,583,000","Shareholders funds":"62,146,000","Current ratio (x)":"0.99","Profit margin (%)":"29.67","ROE using P/L before tax (%)":"183.01","ROCE using P/L before tax (%)":"56.77","Solvency ratio (Asset based) (%)":"17.63","Number of employees":"161,000"}},"capitalIQ":{"Apple Inc. (NasdaqGS:AAPL)":{"Last  (Delayed)":"193.60","Market Cap (mm)":"3,011,012.8","Open":"195.18","Shares Out. (mm)":"15,552.8","Previous Close":"193.60","Float %":"99.9%","Change on Day":"(1.08)","Shares Sold Short (mm)":"110.7","Change % on Day":"(0.6)%","Dividend Yield %":"0.5%","Day High/Low":"195.41/ 192.97","Diluted EPS Excl. Extra Items":"6.13","52 wk High/Low":"199.62/ 124.17","P/Diluted EPS Before Extra":"31.8x","Volume (mm)":"36.95","Avg 3M Dly Vlm (mm)":"54.62","Beta 5Y":"1.31","Total Revenue":"383,285.0","Market Capitalization":"3,027,809.8","TEV/Total Revenue":"7.8x","EBITDA":"125,820.0","Total Enterprise Value":"2,989,640.8","TEV/EBITDA":"21.1x","EBIT":"114,301.0","Cash & ST Invst.":"61,555.0","Net Income":"96,995.0","Total Debt":"123,930.0","Price/Tang BV":"48.7x","Capital Expenditure":"(10,959.0)","Total Assets":"352,583.0","Total Debt/EBITDA":"0.9x"}}}

  return webscraped_data

  # start_time = time.time()

  # with ThreadPoolExecutor(max_workers=2) as executor:
  #   orbis_future = executor.submit(webscrape_orbis, company)
  #   capitalIQ_future = executor.submit(webscrape_capitalIQ, company)

  # orbis_data = orbis_future.result()
  # capitalIQ_data = capitalIQ_future.result()

  # webscraped_data = {}
  # webscraped_data["orbis"] = orbis_data
  # webscraped_data["capitalIQ"] = capitalIQ_data

  # end_time = time.time()
  # elapsed_time = end_time - start_time
  # print(f"Elapsed time: {elapsed_time}")

  # return webscraped_data

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("concurrency_ThreadPoolExecutor_webscraper:app", host='127.0.0.1', port=5001, reload=True)