import requests
from bs4 import BeautifulSoup
import re

# * Artist Page
default_page = "https://www.azlyrics.com/w/west.html"

# * Example page with <i> tags to show who sings verse
page1 = "https://www.azlyrics.com/lyrics/kanyewest/gorgeous.html"

# * Example page with no <i> tags
page2 = "https://www.azlyrics.com/lyrics/kanyewest/illflyaway.html"

# * To make things modular we need:
# * A function that extracts the verses of a page
# * A function that saves those verses into a txt file


# * Function to extract the lyrics out of an azlyrics webpage
# * Returns a Dictionnary containing artists and their Verses
# ! Only works if page contains an <i> Artist </i> tag
def extract_lyrics(page):
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


# * Just testing if things work as they should
verses = extract_lyrics(page1)
print(verses["Kid Cudi"])
