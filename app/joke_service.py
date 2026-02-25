import requests

class JokeService:
    def __init__(self, api_url):
        self.api_url = api_url

    def get_joke(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            joke_data = response.json()
            return joke_data['joke']
        else:
            return "Error fetching joke"

# Example usage:
# joke_service = JokeService('https://api.jokes.com/random')
# print(joke_service.get_joke())