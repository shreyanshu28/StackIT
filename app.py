from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
from datetime import datetime
import os
import json

load_dotenv()

app = FastAPI()

# Discord bot configuration
DISCORD_WEBHOOK_URL = None

# File to store notifications
NOTIFICATION_FILE = "notifications.txt"

if os.getenv("DISCORD_WEBHOOK_URL"):
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Pydantic model for the notification payload
class Notification(BaseModel):
    Type: str
    Name: str
    Description: str


def write_to_file(notification):
    try:
        with open(NOTIFICATION_FILE, "r") as file:
            notifications = json.load(file)
    except FileNotFoundError:
        notifications = []

    notifications.append(notification)

    with open(NOTIFICATION_FILE, "w") as file:
        json.dump(notifications, file, indent=4)

def read_from_file():
    try:
        with open(NOTIFICATION_FILE, "r") as file:
            notifications = json.load(file)
            return notifications
    except FileNotFoundError:
        return []

@app.post("/notifications")
async def receive_notification(notification: Notification):
    
    if notification.Type == "Warning":
        # Forward the notification to Discord
        if DISCORD_WEBHOOK_URL is None:
            response = send_to_console(notification)
        response = send_to_discord(notification)
        if response == 204:
            return {"message": "Notification forwarded"}
        elif response == 200:
            return {"message": "Notification written to console"}
        else:
            raise HTTPException(status_code=500, detail="Failed to forward notification to Discord")

    elif notification.Type == "Info":
        return {"message": "Notification ignored"}
    else:
        raise HTTPException(status_code=400, detail="Invalid notification type")

@app.get("/notifications")
async def get_notifications():
    return read_from_file()

def send_to_discord(notification: Notification):
    '''
    This function sends the notification to Discord using the Discord webhook URL.
    If the webhook URL is not set, it will print the notification details to the console.

    Ideally the response code should be 200 but Discord sends a response with status code 204 
    if the notification is successfully sent because it isn't recieving any body back.
    '''
    payload = {
        "content": f"**Type**: {notification.Type}\n**Name**: {notification.Name}\n**Description**: {notification.Description}"
    }

    # notification_with_timestamp = {
    #     "timestamp": datetime.now().isoformat(),
    #     "notification": notification.model_dump_json()
    # }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)

    write_to_file({
        "timestamp": datetime.now().isoformat(),
        "notification": notification.model_dump_json(),
        "response": response.status_code
    })

    return response.status_code

def send_to_console(notification: Notification):
    '''
    This function writes the notification details to the console.This is created in the last moments before submitting the project.
    I cannot share my discord via email.
    ''' 
    print(f"Notification Details:\n"
          f"Type: {notification.Type}\n"
          f"Name: {notification.Name}\n"
          f"Description: {notification.Description}")
    
    write_to_file({
        "timestamp": datetime.now().isoformat(),
        "notification": notification.model_dump_json(),
        "response": 200
    })

    return 200