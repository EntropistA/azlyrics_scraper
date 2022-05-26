from collections import namedtuple

from bs4 import BeautifulSoup
import requests

# https://github.com/adhorrig/azlyrics

BASE_URL = "https://www.azlyrics.com"


def get_soup(url: str) -> BeautifulSoup:
    page = requests.get(url).content
    return BeautifulSoup(page, features="html.parser")


ArtistAndLink = namedtuple("ArtistAndLink", "artist link")


def artists_by_letter(letter: str) -> list:
    soup = get_soup(f"{BASE_URL}/{letter.lower()}.html")
    artists_and_links = []
    for div in soup.find_all("div", {"class": "container main-page"}):
        links = div.findAll("a")
        for a in links:
            artists_and_links.append(
                ArtistAndLink(a.text.strip(), a["href"])
            )
    return artists_and_links


def artists_names_by_letter(letter: str) -> list:
    return [artist_and_link.artist for artist_and_link in artists_by_letter(letter)]


def artists_links_by_letter(letter: str) -> list:
    return [artist_and_link.link for artist_and_link in artists_by_letter(letter)]


print(artists_by_letter("a"))
print(artists_names_by_letter("a"))
print(artists_links_by_letter("a"))
