import requests

class MapsApi:
    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.url = "https://www.google.com/maps/search/?api=1&query="

    def get_coordinates_by_search(self):
        r = requests.get(self.url + "lustenau")
        print(r)

if __name__ == "__main__":
    ma = MapsApi("1")