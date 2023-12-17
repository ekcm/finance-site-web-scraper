# Finance site web scraper


<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Finance site web scraper</h3>

  <p align="center">
    A web scraper to scrape Finance sites such as Orbis and CapitalIQ
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

This web scraper was built as a porject to allow Financial Analysts to view company financial information at one site, instead of going to multiple sites to search for information.

## Built With
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Selenium WebDriver](https://www.selenium.dev/) 
* [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Before you can run the application, you must have the following installed

* Python
* FastAPI
* Selenium
* BeautifulSoup4
* dotenv

### Caveats
1. This project uses my own school credentials to log in to Orbis and CapitalIQ. You will need to edit the code to define your own login path.

### Notes
1. I plan to scrape PitchBook in the near future
2. I plan to also develop a frontend and deploy it to allow others access to these financial sites without a subscription.
3. After learning more about concurrency, I hope to also redo the project in Golang (so stay tuned!)

### Learning insights
1. Concurrent.futures library is a great library to experiment and learn about how tasks can be executed in parallel with each other. This saves a substantial amount of time when web scraping from multiple sites at the same time. 


