from collections import namedtuple

from bs4 import BeautifulSoup
import requests

# https://github.com/adhorrig/azlyrics

BASE_URL = "https://www.azlyrics.com"


def get_soup(url: str) -> BeautifulSoup:
    page = requests.get(url).content
    return BeautifulSoup(page, features="html.parser")


Artist = namedtuple("Artist", "name link")
Album = namedtuple("Album", "name songs")
Song = namedtuple("Song", "name link")


def artists_by_letter(letter: str) -> list:
    url = f"{BASE_URL}/{letter.lower()}.html"
    soup = get_soup(url)
    names_and_links = []
    for div in soup.find_all("div", {"class": "container main-page"}):
        links = div.findAll("a")
        for a in links:
            names_and_links.append(
                Artist(a.text.strip(), a["href"])
            )
    return names_and_links


def artists_names_by_letter(letter: str) -> list:
    return [artist.name for artist in artists_by_letter(letter)]


def artists_links_by_letter(letter: str) -> list:
    return [artist.link for artist in artists_by_letter(letter)]


def albums_and_songs(artist_link: str) -> list:
    url = f"{BASE_URL}/{artist_link}"
    soup = get_soup(url)
    albums_names_and_songs = []
    current_album_name = ""
    current_songs = []

    albums_div = soup.find("div", id="listAlbum")
    for div in albums_div.find_all("div"):
        class_ = div.get("class")
        if not class_:
            continue
        if "album" in class_:
            if current_album_name:
                albums_names_and_songs.append(
                    Album(current_album_name, current_songs)
                )
                current_songs = []
            current_album_name = div.find("b").text.strip('"')
        elif "listalbum-item" in class_:
            a = div.find("a")
            current_songs.append(
                Song(a.text, a["href"])
            )
    albums_names_and_songs.append(
        Album(current_album_name, current_songs)
    )
    return albums_names_and_songs


# al = artists_links_by_letter("T")
# print(al[0])
# print(albums_and_songs(al[0]))
# print(dict(albums_and_songs(al[0])))
# print(dict(albums_and_songs(al[0])[0]))
