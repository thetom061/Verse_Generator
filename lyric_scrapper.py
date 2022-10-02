import requests
import json

auth_file = "./auth.json"

url = "https://api.genius.com"

class LyricScrapper: 
    def __init__(self) -> None:   
        with open(auth_file, "r") as f:
            auth_data = json.load(f)
            self.headers={"Authorization":f"Bearer {auth_data['CLIENT ACCESS TOKEN']}"}


    def search(self,key_terms):
        response=requests.get(f"{url}/search",headers=self.headers, params={"q": key_terms}).content
        return json.loads(response)
        



if __name__=="__main__": 
    scrapper=LyricScrapper()
    print(scrapper.search("Kanye West"))
