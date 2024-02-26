from typing import List, Dict

from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

from helpers.DocumentFormater import DocumentFormater
from datetime import datetime


load_dotenv('config/open.env')

with open('config/roles/role.txt', 'r', encoding='UTF-8') as file:
    role = file.read()


class OpenModel:
    def __init__(self):
        self.logging = False
        self.model = getenv('MODEL')
        self.token = getenv('AUTH_TOKEN')
        self.temperature = float(getenv('TEMPERATURE'))
        self.max_tokens = int(getenv('MAX_TOKENS'))
        self.top_p = float(getenv('TOP_P'))

        self.client = OpenAI(api_key=self.token)

        self.messages = []

        self.messages.append({
            'role': 'system',
            'content': role
        })


    def send(self, content: str) -> str:
        message = {'role': 'user', 'content': content}

        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages + [message],
            temperature=self.temperature
        )

        response_content = response.choices[0].message.content

        if self.logging: self._log(response_content)

        return response_content


    def send_file(self, path: str):
        chunks = DocumentFormater.split(path)
        
        results = []
        
        for chunk in chunks:
            resp = self.send(chunk.page_content)
            results.append(resp)
            self._log(resp)
        
        # doc = open(path, 'r', encoding='UTF-8').read()


    def _log(self, content):
        current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        
        with open(f'logs/log_{current_datetime}.txt', 'w', encoding='UTF-8') as log:
            log.write(content)