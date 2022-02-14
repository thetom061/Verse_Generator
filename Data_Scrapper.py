from cgitb import html
import requests
import os
from bs4 import BeautifulSoup

default_page = "https://www.azlyrics.com/w/west.html"


page = "https://www.azlyrics.com/lyrics/kanyewest/wedontcare.html"
html_text = requests.get(page).content
soup = BeautifulSoup(html_text, "html.parser")

# manages to find the lyrics
for lyrics in soup.find_all("div", {"class": None, "id": None}):
    print(lyrics)
