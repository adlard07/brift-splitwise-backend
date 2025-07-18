from splitwise import Splitwise
from splitwise.exception import SplitwiseException
from dotenv import load_dotenv
import json
import os

from utils.logger import logging

load_dotenv()

class SplitwiseAuthInitializer:
    def __init__(self):
        """Initialize Splitwise authentication with environment variables."""
        self.consumer_key = os.getenv('CUSTOMER_KEY')
        self.consumer_secret = os.getenv('CUSTOMER_SECRET')
        self.api_key = os.getenv('API_KEY')  # Optional, for API v3
        if not all([self.consumer_key, self.consumer_secret]):
            logging.error("Missing CONSUMER_KEY or CONSUMER_SECRET in environment variables.")
            raise ValueError("Required environment variables are missing.")
        # logging.info("SplitwiseAuthInitializer initialized with environment variables.")


    def create_splitwise_obj(self):
        """Create and return a Splitwise object."""
        try:
            s_obj = Splitwise(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                api_key=self.api_key
            )
            logging.info("Splitwise object created successfully.")
            return s_obj
        except Exception as e:
            logging.error(f"Failed to create Splitwise object: {str(e)}")
            raise

    def get_authorize_url(self, s_obj):
        """Get OAuth authorization URL and secret."""
        try:
            url, secret = s_obj.getAuthorizeURL()
            logging.info(f"Authorization URL generated: {url}")
            return url, secret
        except SplitwiseException as e:
            logging.error(f"Failed to get authorization URL: {str(e)}")
            raise

    def get_access_token(self, s_obj, oauth_token, oauth_token_secret, oauth_verifier):
        """Retrieve access token using OAuth credentials."""
        try:
            access_token = s_obj.getAccessToken(
                oauth_token=oauth_token,
                oauth_token_secret=oauth_token_secret,
                oauth_verifier=oauth_verifier
            )
            logging.info("Access token retrieved successfully.")
            return access_token
        except SplitwiseException as e:
            logging.error(f"Failed to retrieve access token: {str(e)}")
            raise


    def save_credentials(self, creds, filename):
        """Save credentials to a JSON file."""
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w') as f:
                json.dump(creds, f, indent=4)
            logging.info(f"Credentials saved to {filename}.")
        except (IOError, PermissionError, TypeError) as e:
            logging.error(f"Failed to save credentials: {str(e)}")
            raise


    def load_credentials(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return data
            logging.info(f'Credentials loaded from {filename}')
        except Exception as e:
            logging.error(f"Failed to load credentials. Error occured: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        # Initialize SplitwiseAuthInitializer
        auth = SplitwiseAuthInitializer()
        s_obj = auth.create_splitwise_obj()

        # Step 1: Get authorization URL and secret
        url, secret = auth.get_authorize_url(s_obj)
        logging.info(f"Please visit this URL to authorize the application: {url}")
        creds['secret'] = secret

        oauth_token = input("Enter oauth_token from callback: ")
        oauth_verifier = input("Enter oauth_verifier from callback: ")
        creds['oauth_token'] = oauth_token
        creds['oauth_verifier'] = oauth_verifier

        # Step 3: Get access token
        access_token = auth.get_access_token(
            s_obj,
            oauth_token=creds['oauth_token'],
            oauth_token_secret=creds['secret'],
            oauth_verifier=creds['oauth_verifier']
        )
        creds['access_token'] = access_token

        # Set access token for Splitwise object
        s_obj.setAccessToken(creds['access_token'])

        s_obj.getCurrentUser()

    except Exception as e:
        logging.error(f"Script execution failed: {str(e)}")
        print(f"An error occurred: {str(e)}")