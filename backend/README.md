This is a Python [FastAPI](https://fastapi.tiangolo.com/) project, with 2 main Python files as of now:
* sequential_webscraper.py : to test scraping from Orbis and CapitalIQ sequentially (in that order)
* concurrenty_ThreadPoolExecutor_webscraper.py : to test scraping from Orbis and CapitalIQ concurrently using the concurrent.futures Python library.

### Setup
Create a .env file and place it in the backend folder:
```
email=''
password=''
```
The .env file will be gitignored and will not be pushed into your repository.

To run the development server:
```
cd backend
python sequential_webscraper.py
python concurrency_ThreadPoolExecutor_webscraper.py
```
This will open http://127.0.0.1:5000 for sequential_webscraper.py and http://127.0.0.1:5001 for concurrency_ThreadPoolExecutor_webscraper.py respectively. 

### Usage
To run the webscraper, go to http://127.0.0.1:5001/api/webscrape/{company} and replace {companny} with the company name. For example, if you want to search for the financials for apple, you would use:
```
http://127.0.0.1:5001/api/webscrape/apple
```

Currently the webscraper runs headless. If you want to visualise the steps taken by the webscraper, uncomment this line 36:
```
chrome_options.add_argument('--headless')
```



