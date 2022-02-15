import requests
from bs4 import BeautifulSoup
import re

# * Artist Page
default_page = "https://www.azlyrics.com/w/west.html"

# * Example page
page = "https://www.azlyrics.com/lyrics/kanyewest/gorgeous.html"


# * Function to extract the lyrics out of an azlyrics webpage
# ! Doesn't differentiate depending on Artist, need to be implemented
# ! Maybe use dictionnary to return lyrics so every verse is tied to an artist
def extract_lyrics(page):
    html_text = requests.get(page).content
    soup = BeautifulSoup(html_text, "html.parser")
    for lyrics in soup.findAll("div", {"class": None, "id": None}):
        for artist in lyrics.findAll("i"):
            tag = artist.nextSibling
            verse = ""
            while (re.match("(<i>.*</i>)", str(tag)) is None):
                if (str(tag) != "<br/>"):
                    verse += str(tag)
                if (tag.nextSibling is None):
                    break
                tag = tag.nextSibling
            print(verse)


# * Just testing if things work as they should
extract_lyrics(page)
