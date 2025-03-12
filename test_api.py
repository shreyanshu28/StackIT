from fastapi.testclient import TestClient
from app import app

# Create a test client for the app
client = TestClient(app)

def test_post_warning_notification():
    # Mock "Warning" notification payload
    warning_notification = {
        "Type": "Warning",
        "Name": "Backup Failure",
        "Description": "The backup failed due to a database problem"
    }
    # Make POST request to the /notifications endpoint
    response = client.post("/notifications", json=warning_notification)
    
    # Assertions
    '''THe resason it is not 204 is because the test file gets response from the endpoint and not from discord.'''
    assert response.status_code == 200  # Verify HTTP status code
    assert response.json() == {"message": "Notification forwarded"}

def test_post_info_notification():
    # Mock "Info" notification payload
    info_notification = {
        "Type": "Info",
        "Name": "Quota Exceeded",
        "Description": "Compute quota exceeded the allowed limit"
    }
    # Make POST request to the /notifications endpoint
    response = client.post("/notifications", json=info_notification)
    
    # Assertions
    assert response.status_code == 200  # Verify HTTP status code
    assert response.json() == {"message": "Notification ignored"}

def test_post_invalid_type_notification():
    # Mock invalid notification payload
    invalid_notification = {
        "Type": "Critical",  # Unsupported type
        "Name": "Security Breach",
        "Description": "Unauthorized access detected"
    }
    # Make POST request to the /notifications endpoint
    response = client.post("/notifications", json=invalid_notification)
    
    # Assertions
    assert response.status_code == 400  # Verify HTTP status code
    assert response.json() == {"detail": "Invalid notification type"}
