import requests
import json

from discord.authobjects.User import userobj
from discord.authobjects.Access import accessobj


class Oath:
    def __init__(self, token, client_id, client_secret, redirect_uri):
        self.token = token
        # self.validate_token: bool = True

        self.client_id = client_id
        self.client_secret = client_secret

        self.redirect_uri = redirect_uri
        self.headers = {
            "Authorization": "Bot {}".format(self.token),
            "User-Agent": "myBotThing (http://some.url, v0.1)",
            "Content-Type": "application/json",
        }

        self.oath_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope=identify"
        self.base_url = "https://discord.com/api/v9"

        self.access = None

    def validate_token(self) -> None:
        try:
            baseURL = "https://discord.com/api/v9" + "/users/@me"
            r = requests.get(baseURL, headers=self.headers)
            request_json = json.loads(r.text)
        except:
            raise "Invalid token has been passed"

    def get_access_token(self, code, redirect_uri):
        redirect_uri = redirect_uri
        url = self.base_url + "/oauth2/token"
        current_user = self.get_current_user()

        data = {
            "client_id": current_user.id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        r = requests.post(url, headers=headers, data=data)
        request_json = json.loads(r.text)

        self.access = accessobj(request_json)
        return self.access

    def refresh_access_token(self, refresh_token):
        url = self.base_url + "/oauth2/token"
        current_user = self.get_current_user()

        data = {
            "client_id": current_user.id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }

        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        r = requests.post(url, headers=headers, data=data)
        request_json = json.loads(r.text)

        self.access = accessobj(request_json)
        return self.access

    def get_current_user(self):
        url = self.base_url + "/users/@me"
        r = requests.get(url, headers=self.headers)
        request_json = json.loads(r.text)

        return userobj(request_json)

    def get_user_data(self):
        user_headers = {
            "Authorization":
            "{} {}".format(self.access.token_type, self.access.token)
        }

        url = self.base_url + "/users/@me"
        r = requests.get(url, headers=user_headers)
        request_json = json.loads(r.text)
        print(request_json)
        return userobj(request_json)
