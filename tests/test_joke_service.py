import unittest
from joke_service import get_joke  # Assuming this is the function of the joke service

class TestJokeService(unittest.TestCase):
    def test_get_joke(self):
        joke = get_joke()
        self.assertIsInstance(joke, str)
        self.assertGreater(len(joke), 0, "Joke should not be empty")

if __name__ == "__main__":
    unittest.main()