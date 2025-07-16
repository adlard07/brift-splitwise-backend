from fastapi import FastAPI, Request
import json


def save_oauth_creds(creds: dict):
	with open("creds.json", 'w') as f:
		json.dump(creds, f, indent=4)

app = FastAPI()

@app.get("/callback")
async def callback(request: Request):
    params = save_oauth_creds(dict(request.query_params))
    return params