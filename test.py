
from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY") 

import openai

from openai import OpenAI
client = OpenAI()

print(client.models.list())

