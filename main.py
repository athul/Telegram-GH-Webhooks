from fastapi import FastAPI, Request
import os
import httpx
from typing import Dict

app = FastAPI()

TOKEN = os.getenv("TOKEN")  # Telegram Bot API Key
CHAT_ID = os.getenv("CHAT_ID")  # Telegram Chat ID


@app.get("/")
async def hello():
    return "Hello World"


async def sendMessage(message: str) -> Dict:
    """
    Sends the Message to telegram with the telegram API
    """
    print(message)
    tg_msg = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        resp = await client.post(API_URL,json=tg_msg)
    print(resp.json())
    return resp.json()


@app.post("/hook")
async def recWebHook(req: Request) -> str:
    """
    Receive the Webhook and process the Webhook Payload to get relevant data
    Refer https://developer.github.com/webhooks/event-payloads for all GitHub Webhook Events and Payloads

    """
    body = await req.json()
    print(body)
    event = req.headers.get("X-Github-Event")
    if event == "star":
        nos_stars = body["repository"]["stargazers_count"]
        starrer_username = body["sender"]["login"]
        repo_url = body["repository"]["html_url"]
        repo_name = body["repository"]["name"]
        message = f"{starrer_username} has starred the [{repo_name}]({repo_url}). \n\n The Total Stars are {nos_stars}"
        return await sendMessage(message)
    elif event == "pull_request":
        pr_number = body["number"]
        pr_title = body["repository"]["title"]
        pr_desc = body["repository"]["body"]
        pr_login = body["repository"]["sender"]["login"]
        pr_login_url = body["repository"]["sender"]["html_url"]
        pr_url = body["repository"]["html_url"]
        message = f"New Pull Request([{pr_number}]({pr_url})) opened by [{pr_login}](pr_login_url).\n\n Title: {pr_title} \n\n Description: {pr_desc}"
        return await sendMessage(message)
