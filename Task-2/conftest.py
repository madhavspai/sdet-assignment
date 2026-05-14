import pytest
import requests
 
 
@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"
 
 
@pytest.fixture
def get(base_url):
    def _get(endpoint):
        return requests.get(f"{base_url}{endpoint}")
    return _get
 