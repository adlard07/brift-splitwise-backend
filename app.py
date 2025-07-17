from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import json

from utils.auth import SplitwiseAuthInitializer


def save_oauth_creds(creds: dict):
	with open("creds.json", 'w') as f:
		json.dump(creds, f, indent=4)

app = FastAPI()

@app.get('/redirect')
async def redirect(request: Request):
	auth = SplitwiseAuthInitializer()
	s_obj = auth.create_splitwise_obj()
	redirect_url, secret = auth.get_authorize_url(s_obj)
    creds['secret'] = secret

	access_token = auth.get_access_token(
		s_obj,
		oauth_token=creds['oauth_token'],
		oauth_token_secret=creds['secret'],
		oauth_verifier=creds['oauth_verifier']
		)
    creds['access_token'] = access_token	
	return RedirectResponse(url=redirect_url, status_code=302)


@app.get("/callback")
async def callback(request: Request):
    params = dict(request.query_params)
    save_oauth_creds(params)
    return None
