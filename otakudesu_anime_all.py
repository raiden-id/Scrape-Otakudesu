import httpx
import re
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor as TPE


@dataclass
class Anime:
    name: str
    title: str
    link: str
    episode: str
    movie: str


class scrape:
    def __init__(self):
        self.mainurl = "https://otakudesu.bid/"
        self.listurl = self.mainurl + 'anime-list'
        self.client = httpx.Client()
        self.episode = []
        self.item = []
        self.parse = BeautifulSoup
        self.get_all_anime()

    def get_all_anime(self):
        response = self.client.get(self.listurl)
        parse = self.parse(response.text, 'html.parser')
        logs = parse.find_all('a', {'class': 'hodebgst'})
        with TPE(max_workers=30) as ex:
            for i in logs:
                print(f"URL: {i['href']}")
                episode = self.get_all_episode(i['href'])
                movie = self.get_all_lengkap(i['href'])
                item = Anime(
                    name=i.text,
                    title=i['title'],
                    link=i['href'],
                    episode=episode,
                    movie=movie
                )
                self.item.append(asdict(item))

#            open('database.txt', 'w', encoding="utf-8").write(str(self.item))
            print(self.item)

    def get_all_episode(self, link):
        episode = []
        response = self.client.get(link)
        parse = self.parse(response.text, 'html.parser')
        for i in parse.findAll('a'):
            if "episode" in i.get('href'):
                episode.append(i.get('href'))

        print(f"FULEP: OK")
        return episode

    def get_all_lengkap(self, link):
        lengkap = []
        response = self.client.get(link)
        parse = self.parse(response.text, 'html.parser')
        for i in parse.findAll('a'):
            if "lengkap" in i.get('href'):
                lengkap.append(i.get('href'))

        print(f"ALL: OK")
        return lengkap


scrape()
