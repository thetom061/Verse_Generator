import requests
from bs4 import BeautifulSoup
import re
import os

# * Artist Page
default_page = "https://www.azlyrics.com/w/west.html"

# * Example page with <i> tags to show who sings verse
page1 = "https://www.azlyrics.com/lyrics/kanyewest/gorgeous.html"

# * Example page with no <i> tags
page2 = "https://www.azlyrics.com/lyrics/kanyewest/illflyaway.html"

# * Function to extract the lyrics out of an azlyrics webpage
# * Returns a Dictionnary containing artists and their respective Verses


def scrape_lyrics(page):
    verses = {}
    html_text = requests.get(page).content
    soup = BeautifulSoup(html_text, "html.parser")

    # We grab lyrics
    for lyrics in soup.findAll("div", {"class": None, "id": None}):
        verse = ""
        # Loop through artists singing the song
        for artist in lyrics.findAll("i"):
            # To keep only the names of the singers
            singers = re.sub("[\[\]:]", '', artist.text)
            # we want to point to next element aka lyrics
            tag = artist.nextSibling
            # continue looping while the same artist is singing
            while (re.match("(<i>.*</i>)", str(tag)) is None):
                if (str(tag) != "<br/>"):
                    verse += str(tag)
                if (tag.nextSibling is None):
                    break
                tag = tag.nextSibling
            # if the artists already have a verse in the dictionnary, we add the new verse into the list
            if singers in verses:
                verses[singers].append(verse)
            # if singers aren't part of the dictionnary, we add their first verse as a list containing one verse
            else:
                verses[singers] = [verse]
            # reset the verse as
            verse = ""
        # if verses is empty singers aren't specified so we just grab the verse and give it an unknown artist
        if (not verses):
            verses["Unknown"] = [lyrics.get_text()]
    return verses


# * Finds the different song links from an artist home_page in dict
def find_song_links(artist_page, home="https://www.azlyrics.com"):
    html_text = requests.get(artist_page).content
    soup = BeautifulSoup(html_text, "html.parser")
    links = {}
    for song in soup.find_all("div", {"class": "listalbum-item"}):
        # Needed for songs which don't have links
        try:
            url = song.find("a")["href"]
            link = home+url
            links[song.get_text()] = link
        except TypeError:
            pass
    return links

# links is the dict containing link associated to a song


def store_lyrics_to_files(links, filter=None, dir_name=".\Data"):
    try:
        os.mkdir(dir_name)
    except FileExistsError:
        pass
    for song, link in links.items():
        lyrics = scrape_lyrics(link)
        with open(os.path.join(dir_name, f"{song}.txt"), "w") as f:
            for artist in lyrics:
                if filter is None:
                    verses = lyrics[artist]
                    f.write("".join(verses))
            f.close()


store_lyrics_to_files(find_song_links(default_page))
