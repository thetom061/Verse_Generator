import requests
import json

auth_file = "./auth.json"

url = "https://api.genius.com"

class LyricScrapper: 

    def __init__(self) -> None:   
        with open(auth_file, "r") as f:
            auth_data = json.load(f)
            self.headers={"Authorization":f"Bearer {auth_data['CLIENT ACCESS TOKEN']}"}

        self.searched_artist=set()

    def search(self,key_terms):
        response=requests.get(f"{url}/search",headers=self.headers, params={"q": key_terms}).content
        return json.loads(response)
        
    def search_artist_id(self,artist):
        result=self.search(artist)
        artist_id=""
        for hit in result["response"]["hits"]:
            artist_info= hit["result"]["primary_artist"]
            user_in=input(f"Press 1 if {artist_info['name']} is the artist you are looking for\n")
            if int(user_in)==1:
                artist_id=artist_info["id"]
                print(artist_id)
                self.searched_artist.add(artist_id)
                break
                
                




if __name__=="__main__": 
    scrapper=LyricScrapper()
    scrapper.search_artist_id("Taylor Swift")
