from fastapi import testclient
from app import app

client = testclient.TestClient(app)

# Test the summarize endpoint
def test_summarize():
    response = client.post("/summarize", data={"text": "Artificial intelligence (AI) is a branch of computer science focused on creating machines capable of intelligent behavior. It includes areas like machine learning, natural language processing, computer vision, robotics, and expert systems. AI technologies are now widely applied in healthcare, finance, transportation, and many other sectors, helping humans make better decisions and automate complex tasks."})
    assert response.status_code == 200
    assert "summary" in response.json()