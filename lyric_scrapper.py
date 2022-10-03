import requests
import json
from bs4 import BeautifulSoup


class LyricScrapper: 

    def __init__(self,url="https://api.genius.com",auth_file="./auth.json") -> None:
        self.url=url
        with open(auth_file, "r") as f:
            auth_data = json.load(f)
            self.headers={"Authorization":f"Bearer {auth_data['CLIENT ACCESS TOKEN']}"}

        self.searched_artist=set()
        self.song_ids=set()

    def search(self,key_terms):
        response=requests.get(f"{self.url}/search",headers=self.headers, params={"q": key_terms}).content
        return json.loads(response)
        
    def search_artist_id(self,artist):
        result=self.search(artist)
        artist_id=""
        for hit in result["response"]["hits"]:
            artist_info= hit["result"]["primary_artist"]
            artist_name=artist_info['name']
            user_in=input(f"Press 1 if {artist_name} is the artist you are looking for\n")
            if int(user_in)==1:
                artist_id=artist_info["id"]
                self.searched_artist.add((artist_id,artist_name))
                break

    # TODO Right now it just gets the id of everysong on the first page regardless if actual song or not + needs to be able to go to the other pages
    def get_artist_songs(self,artist_info):
        (artist_id,artist_name)=artist_info
        response=json.loads(requests.get(f"{self.url}/artists/{artist_id}/songs",headers=self.headers).content)
        print(response)
        for song in response["response"]["songs"]:
            self.song_ids.add(song["id"])

    # TODO Right now we can get lyrics, work on taking the verse information out of it 
    def get_song_lyrics(self,song_id):
        response=json.loads(requests.get(f"{self.url}/songs/{song_id}",headers=self.headers).content)
        genius_url=response["response"]["song"]["url"]
        response=requests.get(genius_url).content
        soup=BeautifulSoup(response,"html.parser")
        lyrics_container=soup.find(attrs={"data-lyrics-container":"true"})
        lyrics=lyrics_container.get_text(separator="\n")



    # TODO where whole pipeline is going to be executed
    def fast_get():
        
        pass


                

if __name__=="__main__": 
    scrapper=LyricScrapper()
    scrapper.get_song_lyrics(3780008)
