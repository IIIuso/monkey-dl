import requests
from Color import Color
from Color import printer
from bs4 import BeautifulSoup

class Episode :
    def __init__(self, title, episode):
        self.title = title
        self.episode = episode
        self.id = None
        self.page_url = None
        self.download_url = None


def extract_episode_names(url, isFiller, start_epi, end_epi) :
    printer("INFO", "Collecting episode names...")
    episodes = []

    session = requests.Session()

    page = session.get(url).content
    soup_html = BeautifulSoup(page, "html.parser")

    table = soup_html.find("table", attrs={"class" : "EpisodeList"}).find("tbody")

    if isFiller :
        epis = table.findAll("tr")
    else :
        epis = table.findAll("tr", attrs={"class" : ["anime_canon", "mixed_canon/filler", "manga_canon"]})
    
    for epi in epis :
        epi_no = int(epi.find("td", attrs={"class" : "Number"}).text)

        if epi_no < start_epi :
            continue

        if epi_no > end_epi :
            break

        title = epi.find("td", attrs={"class" : "Title"}).find("a").text
        episode = Episode(title, "Episode - " + str(epi_no))

        episodes.append(episode)
        # print(episode.episode, ":", episode.title)
    
    printer("INFO", "Successfully collected episode names!")
    return episodes

