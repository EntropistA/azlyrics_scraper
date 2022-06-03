# azlyrics-scraper

azlyrics-scraper is a Python library for extracting data from [AZLyrics](https://www.azlyrics.com)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install azlyrics-scraper

```bash
pip install azlyrics-scraper
```

## Usage

### Importing

```python
import azlyrics-scraper
```

### Basic usage

#### Finding lyrics

```python
# returns 
azlyrics_scraper.find_lyrics_by_song_title("Runaway")

# returns 
azlyrics_scraper.find_full_lyrics_by_lyrics_fragment("I was running far away")
```

#### Finding a Song

```python
# returns 
azlyrics_scraper.find_song_by_title("Cure for me")

# returns 
azlyrics_scraper.find_song_by_lyrics_fragment("cause I don't need a cure")
```

#### Finding an Artist

```python
# returns Artist(name='AURORA', link='https://www.azlyrics.com/a/aurora.html')
azlyrics_scraper.find_artist_by_name("Aurora")
```

#### Finding an Album

```python
# returns Album(title='The Gods We Can Touch',
# album_link='https://www.azlyrics.com/a/aurora.html#101389',
# songs=[Song(title='The Forbidden Fruits Of Eden',
# ...
# )
azlyrics_scraper.find_album_by_title("The Gods We Can Touch")
```

### Used classes and their attributes

* Artist: name, link
* Album: title album_link, songs
* Song: title, link
* Search: songs_results, artist_results, albums_results, lyrics_results

### Finding links

Each of classes has a `.link` attribute which can be used to get link from _find_ results

### Proxy configuration
In order to use proxy connection set `_proxies` variable to your proxies dictionary
```python
proxies = {
        "http": "http://example.com:8886",
        "https": "https://example.com:8887"
}
azlyris_scraper._proxies = proxies
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
