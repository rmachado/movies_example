# Movies Example

## Set up - Using Docker

```
docker build -t movies_example .
docker run -d -p 80:80 movies_example
```

Then load http://localhost/movies on the browser

## Set up - No Docker

1. Create a virtual env and install dependencies
```
virtualenv env
pip install -Ur requirements.txt
```

2. Run the scrapers to fetch the movie reviews (this might take a while)
```
cd movies_scraper
scrapy crawl IMDb -t json -o scraped/imdb.json
scrapy crawl metacritic -t json -o scraped/metacritic.json
scrapy crawl rottentomatoes -t json -o scraped/rottentomatoes.json
```

3. Initialize the Django database and import the scraped data
```
cd ../movies_site
python manage.py migrate
python manage.py importdata ../movies_scraper/scraped/imdb.json
python manage.py importdata ../movies_scraper/scraped/metacritic.json
python manage.py importdata ../movies_scraper/scraped/rottentomatoes.json
```

4. Run the Django project
```
python manage.py runserver
```