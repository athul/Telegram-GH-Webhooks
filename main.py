from fastapi import FastAPI, Request
import os
import httpx

app = FastAPI()

TOKEN = os.getenv("TOKEN")  # Telegram Bot API Key
CHAT_ID = os.getenv("CHAT_ID")  # Telegram Chat ID

async def sendTgMessage(message: str):
    """
    Sends the Message to telegram with the Telegram BOT API
    """
    print(message)
    tg_msg = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    async with httpx.AsyncClient() as client:
        resp = await client.post(API_URL, json=tg_msg)
    print(resp.json())


@app.post("/hook")
async def recWebHook(req: Request):
    """
    Receive the Webhook and process the Webhook Payload to get relevant data
    Refer https://developer.github.com/webhooks/event-payloads for all GitHub Webhook Events and Payloads
    """
    body = await req.json()
    print(body)
    event = req.headers.get("X-Github-Event")
    if event == "star":  # check if the event is a star
        nos_stars = body["repository"]["stargazers_count"]
        starrer_username = body["sender"]["login"]
        repo_url = body["repository"]["html_url"]
        repo_name = body["repository"]["name"]
        message = f"{starrer_username} has starred the [{repo_name}]({repo_url}). \n\n The Total Stars are {nos_stars}"
        await sendTgMessage(message)
    elif event == "pull_request":  # check if event is a pull request
        pr_number = body["number"]
        if body["pull_request"]["merged"] == True:
            pr_action = "merged"
        pr_action = body["action"]
        pr_title = body["pull_request"]["title"]
        pr_desc = body["pull_request"]["body"]
        pr_login = body["sender"]["login"]
        pr_login_url = body["sender"]["html_url"]
        pr_url = body["pull_request"]["html_url"]
        message = f"Pull Request([{pr_number}]({pr_url})) {pr_action} by [{pr_login}]({pr_login_url}).\n\n Title: *{pr_title}* \n\n Description: **{pr_desc}**"
        await sendTgMessage(message)
