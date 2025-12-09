import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    response = client.post("/activities/Chess Club/signup?email=tester@mergington.edu")
    assert response.status_code == 200
    assert "Signed up tester@mergington.edu for Chess Club" in response.json()["message"]


def test_signup_already_signed_up():
    # First sign up
    client.post("/activities/Gym Class/signup?email=already@mergington.edu")
    # Try again
    response = client.post("/activities/Gym Class/signup?email=already@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_full():
    # Fill up activity
    max_participants = activities["Debate Team"]["max_participants"]
    current_participants = len(activities["Debate Team"]["participants"])
    for i in range(max_participants - current_participants):
        client.post(f"/activities/Debate Team/signup?email=full{i}@mergington.edu")
    response = client.post("/activities/Debate Team/signup?email=overflow@mergington.edu")
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]


def test_signup_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=ghost@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
