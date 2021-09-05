from numpy.testing._private.utils import tempdir
import requests
import os
import json
import fake_useragent
from requests.api import request
import pandas as pd
from slugify import slugify

class StreetFinder():   
    def __init__(self):
        self.url = "https://www.statistik.at/statistik.at/strassen/#/strassenGemeindeOutput"
        self.towns = pd.read_csv("data/towns.csv")

    def get_response_by_town(self, town):
 
        os.system("curl -o Vorarlberg/json/"+slugify(str(town["name"]))+".json 'https://www.statistik.at/statistik.at/strassenRest/getStrassenData' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/json' -H 'Origin: https://www.statistik.at' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Referer: https://www.statistik.at/statistik.at/strassen/' -H 'Cookie: JSESSIONID=E30C4AC6151A6E1D9868E29B871097E4; f5avraaaaaaaaaaaaaaaa_session_=OIJFGGPLLKJGMGLHCHEADCGPGBOENDGGOILFGDEMNICPIBPCIAEGPJADDCFOJPGDPPKDMEIHCBILBLEHLBGAAKPHIBIPODDMBMLHPADMIGLAHLNFDEACNBGBDLANKHPL; f5avraaaaaaaaaaaaaaaa_session_=IJEBCCGJMIOECGKHALCINCCAOIFBGIMNBNNMEMCLGJDPPNAFFHDAPFADEJPJFDGCPOCDGCPONBLOJBAKMDBACMKKJBFHJKMCPOLFDCIDHMGMFOBBBIJLILKJMHBFDBBO' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' --data-raw '{\"ort\":"+str(town['gkz'])+",\"strasse\":\"\",\"bundesland\":\"\"}'")
        
        

    def search_all_towns(self):
        for index, town in self.towns.iterrows():
            self.get_response_by_town(town)

    def town_json2csv(self):
        
        for index, town in self.towns.iterrows():
            f = open("Vorarlberg/json/"+slugify(str(town["name"]))+".json")
            data = json.load(f)
            

            streets = []
            for street in data['result']:
                print(streets)
                streets.append(street)
            df = pd.DataFrame(streets)
            print(df)
            df.to_csv("Vorarlberg/csv/"+slugify(str(town["name"]))+".csv")
    
    
    def extract_streetnames(self):
        for index, town in self.towns.iterrows():

            df = pd.read_csv("Vorarlberg/csv/"+slugify(str(town["name"]))+".csv")
            df["stroffi"].to_csv("Vorarlberg/csv/streetnames/"+slugify(str(town["name"]))+".csv")
if __name__ == "__main__":
    sf = StreetFinder()
    sf.search_all_towns()
    sf.town_json2csv()
    sf.extract_streetnames()


