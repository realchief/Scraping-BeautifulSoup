from bs4 import BeautifulSoup
import requests
from urlparse import urlparse


def get_arg(index, default=None):

    try:
        return sys.argv[index]
    except IndexError:
        return default


class Search(object):
    def __init__(self, url):
        self.url = url

    def getSoupFile(self):
        try:
            return BeautifulSoup(requests.get(self.url).text)
        except:
            return None

    def getBaseUrl(self):
        Url = urlparse(self.url)
        baseUrl = Url.scheme + "://" + Url.netloc
        return baseUrl


class ScrapingFilmList(Search):
    def __init__(self, url):
        super(ScrapingFilmList, self).__init__(url)

    def getFilmList(self):
        soup = self.getSoupFile()
        if soup is None:
            return list()

        filmlists = soup.findAll("div", {"class": "item-img"})

        urls = []
        for filmlist in filmlists:
            url = filmlist.a['href']
            if 'http' not in url:
                url = self.getBaseUrl() + url
            urls.append(url)

        return urls


class CrawlFilmEpisodeList(Search):
    def __init__(self, url):
        super(CrawlFilmEpisodeList, self).__init__(url)

    def getAllFilmEpisodeUrls(self):
        episodeurls = []

        soup = self.getSoupFile()

        seasonlist = soup.findAll("div", {"class": "episodes-list"})

        for season in seasonlist:
            episodelist = season.findAll("li")
            for episode in episodelist:
                url = episode.a['href']
                if 'http' not in url:
                    url = self.getBaseUrl() + url
                episodeurls.append(url)

        return episodeurls

    def getFilmInfo(self, filter_url):
        filmInfo = dict()

        soup = self.getSoupFile()

        seasonlist = soup.findAll("div", {"class": "episodes-list"})

        for season in seasonlist:
            episodelist = season.findAll("li")
            for episode in episodelist:
                url = episode.a['href']
                if 'http' not in url:
                    url = self.getBaseUrl() + url
                if filter_url == url:
                    seasonInfo = season.find('div', {'class': 'season-num'}).text
                    filmInfo['Season'] = seasonInfo.split(' ')[1]
                    filmInfo['Episode'] = episode.find('span', {'class': 'epnum'}).text
                    break
        return filmInfo


class CrawlFilmEpisodeInfo(Search):
    def __init__(self, url, base_data):
        super(CrawlFilmEpisodeInfo, self).__init__(url)
        self.ep_data = base_data

    def getEpisodeInfo(self):
        episodeinfo = self.ep_data
        resultlinks = []

        soup = self.getSoupFile()
        title = soup.title.text

        episodeinfo['title'] = title.split(" - ")[0]

        episodelinks = soup.findAll("iframe")
        for episodelink in episodelinks:
            resultlinks.append((episodelink)['src'])

        episodeinfo['links'] = resultlinks

        return episodeinfo


if __name__ == '__main__':
    if get_arg(1):
        keyword = get_arg(1)
    else:
        keyword = raw_input("=====Type Input Keyword====")
    url = "http://myputlocker.me/?s=" + keyword
    data = ScrapingFilmList(url)
    filmlist = []
    filmlist += data.getFilmList()

    for filmurl in filmlist:
        episodecrawler = CrawlFilmEpisodeList(filmurl)
        allepisodeurl = episodecrawler.getAllFilmEpisodeUrls()

        for episodeurl in allepisodeurl:
            filminfo = episodecrawler.getFilmInfo(episodeurl)
            episodeInofCrawler = CrawlFilmEpisodeInfo(episodeurl, filminfo)
            print(episodeInofCrawler.getEpisodeInfo())
