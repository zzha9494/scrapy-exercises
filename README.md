# Scrapy Exercises

This repository is for practicing [Scrapy](https://scrapy.org/), a free and open-source web-crawling framework, and thanks to the people who gave me this valuable opportunity.

## Requirements

- Python 3.8+
- scrapy 2.11

## Getting Started (For Windows)

1.  Create a Python virtual environment, which helps isolate the practice environment from the main environment and reduces the possibility of package conflicts.

        python -m venv my_scrapy_env

2.  Activate the virtual environment.

        my_scrapy_env/Scripts/activate

3.  Install dependencies.

        pip install -r requirements.txt

    This will install packages from _requirements.txt_:

    - scrapy
    - shub
    - scrapy-crawlera
    - google-cloud-storage
    - scrapy-sessions

    **Please note that this project is initialized with Scrapy 2.11. Running `scrapy startproject exercises` with Scrapy 2.4 conflicts with other packages.**

## Usage

**Please note the log level is set to INFO.**

1.  Tackle World

    Inside the _exercises_ folder, run:

        scrapy crawl tackleworldadelaide -O tackleworldadelaide.json

    This generates a json file containing products data from [TackleWorld](https://tackleworldadelaide.com.au/).

2.  Surfboard Empire

    Inside the _exercises_ folder, run:

        scrapy crawl surfboardempire -O surfboardempire.json

    This generates a json file containing products data from [Surfboard Empire](https://www.surfboardempire.com.au/products.json?page=1).

3.  Regular Expressions

    Inside root folder, run:

        python regex.py

    Simply extract the numerical total number of products from an HTML elements.
