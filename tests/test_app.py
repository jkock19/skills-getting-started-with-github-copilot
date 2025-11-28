import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    activity = "Soccer Club"
    email = "student1@mergington.edu"
    # Sign up
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json()["message"]
    # Unregister
    unregister_resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert "Removed" in unregister_resp.json()["message"]

def test_signup_duplicate():
    activity = "Soccer Club"
    email = "student2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Try to sign up again
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]
    # Clean up
    client.post(f"/activities/{activity}/unregister?email={email}")

def test_unregister_not_found():
    activity = "Soccer Club"
    email = "notfound@mergington.edu"
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404
    assert "Participant not found" in resp.json()["detail"]

def test_signup_activity_not_found():
    resp = client.post("/activities/UnknownActivity/signup?email=someone@mergington.edu")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]
