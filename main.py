import requests
from bs4 import BeautifulSoup
import pprint


def get_news(url):
    links = []
    subtext = []

    pagination = 1
    while True:
        res = requests.get(f"{url}?p={pagination}")
        html_data = res.text
        soup = BeautifulSoup(html_data, "html.parser")

        links.append(soup.select(".storylink"))

        print(links[0])
        if not len(links[0]):
            print(links)
            break

        subtext.append(soup.select(".subtext"))
        pagination += 1

    return links, subtext


def sort_news_by_votes(hn):
    return sorted(hn, key=lambda item: item["votes"], reverse=True)


def clean_hn_data(links, subtext):
    hn = ()

    for idx, link in enumerate(links):
        for idx2, link2 in enumerate(link):
            title = link2.getText()

            href = link2.get("href", None)
            vote = subtext[idx][idx2].select(".score")

            if len(vote):
                points = int(vote[0].getText().replace(" points", ""))
            else:
                points = 0

            if points >= 100:
                hn = list(hn)
                hn.append({"title": title, "link": href, "votes": points})
                hn = tuple(hn)

    return sort_news_by_votes(hn)


links, subtext = get_news("https://news.ycombinator.com/news")
pprint.pprint(clean_hn_data(links, subtext))
