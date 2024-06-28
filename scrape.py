import requests
from bs4 import BeautifulSoup
from pprint import pprint
from schedule import every, repeat, run_pending
import time
import os
from dotenv import load_dotenv


load_dotenv()
URL_HEART_BEATS = os.getenv('URL_HEART_BEATS')
# @repeat(every().day.at("02:00", "Europe/Paris"), n=1)
@repeat(every(2).seconds, n=1)
def get_stories(n: int) -> list[dict]:
    url = 'https://news.ycombinator.com/'

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    links = soup.select('.titleline > a')
    scores = soup.select('.score')

    data = []
    for link, score in zip(links, scores):
        #create a dict with the title, url and score
        data.append({
            'title': link.text,
            'url': link.attrs['href'],
            'score': int(score.text.split()[0])
        })

    top_stories = sorted(data, key=lambda x: x['score'], reverse=True)[:n]
    pprint(top_stories)
    requests.get(URL_HEART_BEATS)
    return top_stories


# schedule.every().day.at("02:00", "Europe/Paris").do(get_top_stories)


while True:
    run_pending()
    time.sleep(1)