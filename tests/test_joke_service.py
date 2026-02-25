import unittest
from unittest.mock import patch, MagicMock
from app.joke_service import JokeService


class TestJokeService(unittest.TestCase):
    def test_get_joke(self):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"joke": "Why did the chicken cross the road? To get to the other side!"}

        with patch("app.joke_service.requests.get", return_value=mock_response):
            service = JokeService("https://api.example.com/joke")
            joke = service.get_joke()

        self.assertIsInstance(joke, str)
        self.assertGreater(len(joke), 0, "Joke should not be empty")


if __name__ == "__main__":
    unittest.main()
