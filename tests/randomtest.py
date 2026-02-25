import requests

def test_random_joke_api():
    """Test that the random joke API is working"""
    url = "https://api.api-ninjas.com/v1/jokes?limit=1"
    
    response = requests.get(url)
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Response should contain at least one joke"
    assert "joke" in data[0], "Joke object should contain 'joke' field"
    
    print(f"✓ API test passed. Joke: {data[0]['joke']}")

if __name__ == "__main__":
    test_random_joke_api()