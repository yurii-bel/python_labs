import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from celery import Celery
from celery.schedules import crontab


URL = 'https://news.ycombinator.com/rss'

app = Celery('tasks', broker='localhost')
app.conf.beat_schedule = {
    # Scrapes every 1 minute for testing purposes
    'scraping-task-one-min': {
        'task': 'tasks.scrape',
        'schedule': crontab()
    }
}


@app.task
def save(articles):
    timestamp = datetime.now().strftime('%Y.%m.%d-%H:%M:%S')
    filename = f'output/articles-{timestamp}.json'

    with open(filename, 'w') as f:
        json.dump(articles, f, indent=4)


@app.task
def scrape():
    articles = []

    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, features='xml')
        scraped_articles = soup.findAll('item')

        for a in scraped_articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            article = {
                'title': title,
                'link': link,
                'published': published,
                'created_at': str(datetime.now()),
                'source': 'HackerNews RSS'
            }
            articles.append(article)

        return save(articles)

    except Exception as e:
        print(f'Exception:\n{e}')


# 1. Run rabbitmq server: sudo rabbitmq-server
# 2. Run celery worker: celery -A tasks worker -B -l INFO
