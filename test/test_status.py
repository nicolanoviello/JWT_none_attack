import pytest
import requests

def test_status():
    response = requests.get("http://0.0.0.0:5000/status")
    assert response.content == b'{\n    "message": "Il Sistema non funziona correttamente"\n}\n'
