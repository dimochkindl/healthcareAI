import json
import uuid
from typing import Union
import requests
from requests.auth import HTTPBasicAuth
from core.config import GIGACHAT_CLIENT_SECRET, GIGACHAT_CLIENT_ID, SYSTEM_PROMPT


class GigaChatAPI:

    def __init__(self, token: Union[str, None] = None):
        self.token = token if token is not None else self.get_token()

    def get_token(self):
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        req_id = uuid.uuid4()

        payload = 'scope=GIGACHAT_API_CORP'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': f'{str(req_id)}',
        }
        auth = HTTPBasicAuth(GIGACHAT_CLIENT_ID, GIGACHAT_CLIENT_SECRET)
        response = requests.request("POST", url, headers=headers, data=payload, auth=auth, verify=False)
        token = response.json()['access_token']
        self.token = token
        return token

    async def create_embeddings(self, text: str):
        url = "https://gigachat.devices.sberbank.ru/api/v1/embeddings"
        payload = json.dumps({
            "model": "Embeddings",
            "input": [text]
        })
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response.json()

    async def create_prompt(
            self,
            user_prompt: str,
            system_prompt: str,
            temperature: float = 0.0,
            n: int = 1
    ):
        url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"
        payload = json.dumps({
            "model": "GigaChat-Plus",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": f"Найдите ответ в этом тексте: {system_prompt}\n\nМой вопрос:{user_prompt}",
                }
            ],
            "top_p": 0.47,
            "n": n,
            "stream": False,
            "max_tokens": 6000,
            "repetition_penalty": 1,
            "update_interval": 0
        })

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}',
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        return response.json()
