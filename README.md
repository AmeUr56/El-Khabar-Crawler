
# Elkhabar Crawler

This is a simple Scrapy-based web crawler designed to scrape articles from the Elkhabar website and store them in an SQLite database.

## Features

- Scrapes article details such as title, author, publish date, number of readers, and content.
- Stores scraped data in an SQLite database (`elkhabar_articles.db`).

## Installation

#### 1. Clone the repository:
```
git clone https://github.com/AmeUr56/El-Khabar-Crawler
```
#### 2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Running the Crawler

#### 1. Run the Scrapy spider:
```
scrapy crawl elkhabar_spider
```
#### 2. The data will be inserted into an SQLite database (`elkhabar_articles.db`).

## SQLite Database

The crawler saves article data in the `article` table of the `elkhabar_articles.db` file. The table includes the following columns:
- `title`
- `author`
- `publish_date`
- `number_readers`
- `content`

## Note:
This spider and similar projects are intended for learning purposes only. Please ensure you comply with the website’s terms of service and robots.txt when using the spider.

## License

This project is licensed under the MIT License.
