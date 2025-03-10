import json
import re

from bs4 import BeautifulSoup
from httpx import AsyncClient, Client, HTTPStatusError

BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"


class FirebaseException(Exception):
    pass


class FirebaseAuthClient:
    """
    Client for Firebase Auth REST API
    """
    def __init__(self, api_key: str, app_id: str, user_agent: str = BROWSER_USER_AGENT, access_token: str|None = None, refresh_token: str|None = None):
        self._api_key = api_key
        self._app_id = app_id
        self._client = AsyncClient(headers={
            "User-Agent": user_agent,
            "X-Firebase-gmpid": app_id,
            "Referer": "https://app.evelstar.com",
        })

        self.access_token = access_token
        self.refresh_token = refresh_token

    async def _request(self, url: str, **kwargs) -> dict:
        response = await self._client.post(url, **kwargs)

        try:
            response.raise_for_status()
        except HTTPStatusError as e:
            # Raise a custom exception with the error message from the response
            if 400 <= e.response.status_code < 500:
                raise FirebaseException(e.response.json()["error"]["message"])
            else:
                raise e

        return response.json()

    async def login(self, email: str, password: str, client_type: str = "CLIENT_TYPE_WEB") -> None:
        response_data = await self._request(
            f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self._api_key}",
            json={
                "email": email,
                "password": password,
                "returnSecureToken": True,
                "clientType": client_type,
            }
        )

        self.access_token = response_data["idToken"]
        self.refresh_token = response_data["refreshToken"]

    async def token_refresh(self) -> None:
        response_data = await self._request(
            f"https://securetoken.googleapis.com/v1/token?key={self._api_key}",
            json={
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            }
        )

        self.access_token = response_data["id_token"]
        self.refresh_token = response_data["refresh_token"]


def extract_firebase_config() -> dict|None:
    """
    Method that fetches the html content of the Evelstar app, finds the js index file and extracts the firebase config object
    """
    with Client(base_url="https://app.evelstar.com", headers={"User-Agent": BROWSER_USER_AGENT}, timeout=30) as client:
        response = client.get("/")
        response.raise_for_status()

        # Use BeautifulSoup to parse the html content
        soup = BeautifulSoup(response.text, "html.parser")

        # Search for all script tags and find the first that starts with index- and ends with .js
        script_tags = soup.find_all("script")

        for script_tag in script_tags:
            if script_tag.attrs.get("src") and script_tag.attrs["src"].startswith("/assets/index-") and script_tag.attrs["src"].endswith(".js"):
                index_js_url = script_tag.attrs["src"]
                break
        else:
            raise ValueError("Index.js script tag not found")

        # Fetch the index.js file
        response = client.get(index_js_url)
        response.raise_for_status()

        # Search for all objects that look like the firebase config object
        search = re.findall(r'\{[^{}]+\}', response.text)

        for match in search:
            if "apiKey" in match and "authDomain" in match and "projectId" in match:
                config_str = match
                break
        else:
            raise ValueError("Firebase config object not found in index.js")

        # Fix potential trailing commas and improper JSON formatting
        config_str = re.sub(r',\s*([}\]])', r'\1', config_str)
        config_str = re.sub(r'(`([^`]*)`)', lambda m: f'"{m.group(2).strip()}"', config_str)  # Convert template literals to strings
        config_str = re.sub(r'(?<=[{,])(\s*[a-zA-Z_][a-zA-Z0-9_]*)(?=\s*:)', r'"\1"', config_str)  # Add quotes to keys

        try:
            config = json.loads(config_str)
            return config
        except json.JSONDecodeError as e:
            raise ValueError("Error decoding JSON: " + str(e)) from e


if __name__ == "__main__":
    firebase_config = extract_firebase_config()
    print(firebase_config)
