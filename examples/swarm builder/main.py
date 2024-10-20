from configs.agents import *
from swarm.repl import run_demo_loop

from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


if __name__ == "__main__":
    run_demo_loop(manager_agent, debug=True)
