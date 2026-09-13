from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_cannot_duplicate_signup_for_same_activity():
    activity = "Chess Club"
    original = activities[activity]["participants"][:]
    try:
        response = client.post(f"/activities/{activity}/signup?email=michael@mergington.edu")
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    finally:
        activities[activity]["participants"] = original


def test_unregister_participant_from_activity():
    activity = "Chess Club"
    original = activities[activity]["participants"][:]
    try:
        activities[activity]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

        response = client.delete(f"/activities/{activity}/signup?email=daniel@mergington.edu")
        assert response.status_code == 200
        assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"
        assert "daniel@mergington.edu" not in activities[activity]["participants"]
    finally:
        activities[activity]["participants"] = original
