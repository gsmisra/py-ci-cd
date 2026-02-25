import unittest
from unittest.mock import Mock, patch

from app.joke_service import JokeService

class TestJokeService(unittest.TestCase):
    @patch("app.joke_service.requests.get")
    def test_get_joke(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"joke": "Why did the test pass?"}
        mock_get.return_value = mock_response

        joke_service = JokeService("https://example.com/random")
        joke = joke_service.get_joke()

        self.assertEqual(joke, "Why did the test pass?")

    @patch("app.joke_service.requests.get")
    def test_get_joke_error(self, mock_get):
        mock_get.return_value = Mock(status_code=500)

        joke_service = JokeService("https://example.com/random")
        joke = joke_service.get_joke()

        self.assertEqual(joke, "Error fetching joke")


if __name__ == "__main__":
    unittest.main()
