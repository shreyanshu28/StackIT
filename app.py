from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Discord bot configuration
DISCORD_WEBHOOK_URL = None

if os.getenv("DISCORD_WEBHOOK_URL"):
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# Pydantic model for the notification payload
class Notification(BaseModel):
    Type: str
    Name: str
    Description: str


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

'''
This function sends the notification to Discord using the Discord webhook URL.
If the webhook URL is not set, it will print the notification details to the console.

Ideally the response code should be 200 but Discord sends a response with status code 204 
if the notification is successfully sent because it isn't recieving any body back.
'''
def send_to_discord(notification: Notification):
    payload = {
        "content": f"**Type**: {notification.Type}\n**Name**: {notification.Name}\n**Description**: {notification.Description}"
    }

    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    return response.status_code

'''
This function writes the notification details to the console.This is created in the last moments before submitting the project.
I cannot share my discord via email.
''' 
def send_to_console(notification: Notification):
    print(f"Notification Details:\n"
          f"Type: {notification.Type}\n"
          f"Name: {notification.Name}\n"
          f"Description: {notification.Description}")
    return 200