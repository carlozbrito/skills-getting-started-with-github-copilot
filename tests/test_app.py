from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]

def test_signup_duplicate():
    email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_remove_participant_success():
    email = "emma@mergington.edu"
    response = client.delete(f"/activities/Programming Class/signup", params={"email": email})
    assert response.status_code == 200
    assert f"Removed {email} from Programming Class" in response.json()["message"]

def test_remove_participant_not_found():
    response = client.delete("/activities/Programming Class/signup", params={"email": "notfound@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

def test_remove_participant_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
