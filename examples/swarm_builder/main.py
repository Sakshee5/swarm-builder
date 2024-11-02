from configs.agents import *
from swarm.repl import run_demo_loop

from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY") 

user_name = input("Please Enter Your Name:")
context_variables = {"user_name": user_name}

if __name__ == "__main__":
    run_demo_loop(manager_agent, context_variables=context_variables, stream=True, debug=True)
