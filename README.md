# Finance site web scraper

<div id="top"></div>

<!-- PROJECT LOGO -->
<div align="center">
  <h3 align="center">Finance site web scraper</h3>

  <p align="center">
    A web scraper to scrape Finance sites such as Orbis and CapitalIQ concurrently
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

This web scraper was built as a porject to allow Financial Analysts to view company financial information at one site, instead of going to multiple sites to search for information.

Demo: https://youtu.be/7gkOGdeT8kg

### Built With
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Next.JS](https://nextjs.org/)
* [TailwindCSS](https://tailwindcss.com/)
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

### Roadmap
1. I plan to scrape PitchBook in the near future
2. I plan to redo the web scraper in Golang instead to see if there are significant improvements in concurrency

### Learning insights
1. Web scraping concurrently saves a substantial amount of time. Concurrent.futures library is a great library to experiment and learn about how tasks can be executed in parallel with each other.
#### Overall Comparison

| **Run #**|**Sequential**|**Concurrency**|
|----------|------------|-------------|
| 1        | 74.39663219| 53.191344022|
| 2        | 80.95013141| 46.436173677|
| 3        | 80.40401482| 48.546852352|
| 4        | 70.11545348| 49.301021099|
| 5        | 70.19873809| 45.147296190|
| 6        | 70.71349358| 54.700660705|
| 7        | 74.67209267| 47.320199728|
| 8        | 75.91687726| 47.660172462|
| 9        | 66.36153960| 52.765060186|
| 10       | 73.20582485| 47.976046800|
| Average  | 73.69347980| 49.304482722|

### Sequential Web scraper Results Breakdown
| **Run #**|**Total**|**Orbis**|**CapitalIQ**|
|----------|------------|-------------|-------------|
| 1        | 74.39663219| 48.194565057| 26.200009822|
| 2        | 80.95013141| 46.793831110| 34.154938220|
| 3        | 80.40401482| 53.975790023| 26.426076412|
| 4        | 70.11545348| 43.894196987| 26.219934463|
| 5        | 70.19873809| 43.088206529| 27.108731269|
| 6        | 70.71349358| 44.164463996| 26.546956777|
| 7        | 74.67209267| 48.453665256| 26.215027332|
| 8        | 75.91687726| 49.154812097| 26.759911298|
| 9        | 66.36153960| 39.880728960| 26.479404449|
| 10       | 73.20582485| 47.413989067| 25.789805889|
| Average  | 73.69347980| 46.501424908| 27.190079593|

### Concurrency Web scraper Results Breakdown
| **Run #**|**Total**|**Orbis**|**CapitalIQ**|
|----------|------------|-------------|-------------|
| 1        | 53.19134402| 51.152328014| 28.034861087|
| 2        | 46.43617367| 44.411755800| 26.403929471|
| 3        | 48.54685235| 46.510468482| 26.170239448|
| 4        | 49.30102109| 47.264254331| 28.318347692|
| 5        | 45.14729619| 43.120747327| 24.127367019|
| 6        | 54.70066070| 52.670203924| 25.150769710|
| 7        | 47.32019972| 45.278729915| 25.674119234|
| 8        | 47.66017246| 45.620631694| 23.888689756|
| 9        | 52.76506018| 50.699025154| 28.236309289|
| 10       | 47.97604680| 45.953920841| 27.151864051|
| Average  | 49.30448272| 47.268206548| 26.315649676|

   


