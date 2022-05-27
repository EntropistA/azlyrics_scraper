import string
from collections import namedtuple

from bs4 import BeautifulSoup, Comment
import requests

# TODO: mention
# https://github.com/adhorrig/azlyrics

BASE_URL = "https://www.azlyrics.com"
SEARCH_URL = "https://search.azlyrics.com"


def get_soup(url: str) -> BeautifulSoup:
    page = requests.get(url).content
    return BeautifulSoup(page, features="html.parser")


Artist = namedtuple("Artist", "name link")
Album = namedtuple("Album", "name songs_links")
Song = namedtuple("Song", "name link")
Search = namedtuple("Search", "songs_results artist_results albums_results lyrics_results")


def artists_by_letter(letter: str) -> list:
    url = f"{BASE_URL}/{letter.lower()}.html"
    soup = get_soup(url)
    names_and_links = []
    for div in soup.find_all("div", class_="container main-page"):
        links = div.findAll("a")
        for a in links:
            names_and_links.append(
                Artist(a.text.strip(), f'{BASE_URL}/{a["href"]}')
            )
    return names_and_links


def artists_names_by_letter(letter: str) -> list:
    return [artist.name for artist in artists_by_letter(letter)]


def artists_links_by_letter(letter: str) -> list:
    return [artist.link for artist in artists_by_letter(letter)]


def albums_and_songs(artist_link: str) -> list:
    soup = get_soup(artist_link)

    albums = []
    current_album_name = ""
    current_songs = []

    albums_div = soup.find("div", id="listAlbum")
    albums_div = albums_div if albums_div else soup

    for div in albums_div.find_all("div"):
        class_ = div.get("class")
        if not class_:
            continue

        if "album" in class_:
            if current_album_name:
                albums.append(
                    Album(current_album_name, current_songs)
                )
                current_songs = []
            current_album_name = div.find("b").text.strip('"')

        elif "listalbum-item" in class_:
            a = div.find("a")
            if not a:
                continue

            current_songs.append(
                Song(a.text, f"{BASE_URL}/{a['href']}")
            )

    albums.append(
        Album(current_album_name, current_songs)
    )
    return albums


print(albums_and_songs("https://www.azlyrics.com/e/emilyking.html"))
print(albums_and_songs("https://www.azlyrics.com/a/a1xj1.html"))


def lyrics(song_link: str) -> str:
    url = f"{BASE_URL}/{song_link}"
    soup = get_soup(url)

    lyrics_div = soup.find("div", id=None, class_=None)
    return lyrics_div.text.strip()


# def text_without_punctuation_marks(text: str) -> str:
#     for punctuation_mark in '!"+,-.:?„':
#         text = text.replace(punctuation_mark, "")
#     return text


def text_without_numbering(text: str) -> str:
    return text.strip(string.digits + '. ')


def _song_lyrics_name(name: str):
    return name.split(" - ")[0].strip('"')


def search(term: str) -> Search:
    url = f"{SEARCH_URL}/search.php?q={term}"
    soup = get_soup(url)

    panels = soup.find_all("div", class_="panel")
    songs_results, artists_results, albums_results, lyrics_results = [], [], [], []

    for panel in panels:
        for a in panel.find_all("a", class_=None):
            name = text_without_numbering(a.text)
            if "Song results" in panel.text:
                name = _song_lyrics_name(name)
                songs_results.append(
                    Song(name, a["href"])
                )
            if "Artist results" in panel.text:
                artists_results.append(
                    Artist(name, a["href"])
                )
            if "Album results" in panel.text:
                albums_results.append(
                    Album(name, a["href"])
                ) # TODO: songs links not a link
            if "Lyrics results" in panel.text:
                name = _song_lyrics_name(name)
                lyrics_results.append(
                    Song(name, a["href"])
                )

    return Search(
        songs_results,
        artists_results,
        albums_results,
        lyrics_results,
    )


def find_song_by_lyrics(lyrics_fragment):
    results = search(lyrics_fragment).lyrics_results
    if results:
        return results[0]
    return None


def find_song_by_title(song_title):
    results = search(song_title).songs_results
    if results:
        return results[0]
    return None

# print(find_song_by_lyrics("with the wolves tonight"))
# print(find_song_by_title("with the wolves"))
# print(artists_links_by_letter("a"))
