from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import json
from src.models.auth import SplitwiseAuthInitializer
import os
from utils.logger import logging

app = FastAPI()

@app.get('/redirect')
async def redirect(request: Request):
    try:
        auth = SplitwiseAuthInitializer()
        s_obj = auth.create_splitwise_obj()
        redirect_url, secret = auth.get_authorize_url(s_obj)
        logging.info(f"Redirect url: {redirect_url}")
        logging.info(f"Secret: {secret}")

        creds = {}
        creds['secret'] = secret

        # write db function
        auth.save_credentials(creds, 'data/secret.json')
        logging.info(f"Confirmed secret.json saved at: {os.path.abspath('secret.json')}")
        return RedirectResponse(url=redirect_url, status_code=302)
    except Exception as e:
        logging.error(f"Redirect failed: {str(e)}")
        return {"error": str(e)}, 500


@app.get("/callback")
async def callback(request: Request):
    try:
        auth = SplitwiseAuthInitializer()
        s_obj = auth.create_splitwise_obj()
        
        # read db function
        creds = dict(auth.load_credentials('data/secret.json'))
        logging.info(creds)
        if not creds.get('secret'):
            raise ValueError("No secret found in credentials")

        # Get query parameters from callback
        params = dict(request.query_params)
        oauth_token = params.get('oauth_token')
        oauth_verifier = params.get('oauth_verifier')
        
        if not oauth_token or not oauth_verifier:
            raise ValueError("Missing oauth_token or oauth_verifier in callback")

        # Store oauth_token and oauth_verifier
        creds['oauth_token'] = oauth_token
        creds['oauth_verifier'] = oauth_verifier

        # Get access token
        access_token = auth.get_access_token(
            s_obj,
            oauth_token=creds['oauth_token'],
            oauth_token_secret=creds['secret'],
            oauth_verifier=creds['oauth_verifier']
        )
        creds['access_token'] = access_token

        # write db function
        auth.save_credentials(creds, 'data/auth_token.json')

        # Set access token and verify
        s_obj.setAccessToken(creds['access_token'])
        
        return {
            "access_token": access_token
        }
    except Exception as e:
        logging.error(f"Callback failed: {str(e)}")
        return {"error": str(e)}, 500