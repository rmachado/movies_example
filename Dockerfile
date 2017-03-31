FROM python:3.6-slim

RUN apt-get update && \
    apt-get install -y build-essential libssl-dev && \
    pip install virtualenv

ADD requirements.txt /src/requirements.txt
WORKDIR /src

RUN virtualenv env && \
    pip install -r requirements.txt

ADD . /src

WORKDIR /src/movies_scraper

RUN scrapy crawl IMDb -t json -o scraped/imdb.json && \
    scrapy crawl metacritic -t json -o scraped/metacritic.json && \
    scrapy crawl rottentomatoes -t json -o scraped/rottentomatoes.json

WORKDIR /src/movies_site

RUN python manage.py migrate && \
    python manage.py importdata ../movies_scraper/scraped/imdb.json && \
    python manage.py importdata ../movies_scraper/scraped/metacritic.json && \
    python manage.py importdata ../movies_scraper/scraped/rottentomatoes.json

EXPOSE 80

CMD [ "python", "manage.py", "runserver", "0.0.0.0:80" ]
