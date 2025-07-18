import json
from splitwise import Splitwise

from utils.logger import logging
from src.models.auth import SplitwiseAuthInitializer

class SplitwiseGetUser:
    def __init__(self):
        self.s_obj: Splitwise = SplitwiseAuthInitializer().create_splitwise_obj()
        with open('data/auth_token.json') as f:
            self.oauth = dict(json.load(f))
            self.access_token = self.oauth.get('access_token')
        self.s_obj.setAccessToken(self.access_token)


    def get_self_user(self):
    	user_obj = self.s_obj.getCurrentUser()
    	return {
        	"first_name": user_obj.getFirstName(),
            "last_name": user_obj.getLastName(),
            "email": user_obj.getEmail(),
            "user_pfp": user_obj.getPicture(),
            "registration_status": user_obj.getRegistrationStatus()
        }


    def get_user_details(self, user_obj: Splitwise):
        return {
            "first_name": user_obj.getFirstName(),
            "last_name": user_obj.getLastName(),
            "email": user_obj.getEmail(),
            "user_pfp": user_obj.getPicture(),
            "registration_status": user_obj.getRegistrationStatus()
        }

    def get_friends(self):	
     	self.user_friends = self.s_obj.getFriends()
     	for friend in user_friends:
     		yield self.get_user_details(friend)
     	return user_friends


if __name__ == "__main__":
    s_obj = SplitwiseGetUser()
    logging.info(s_obj.get_user_details())
    # friends = s_obj.get_friends()
    # logging.info(friends)
