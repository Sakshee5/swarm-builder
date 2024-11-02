import os
import json
from swarm import Agent
from typing import List, Dict, Union, Any
import ast
import requests
import requests
from bs4 import BeautifulSoup
import os
import subprocess
import importlib.util
import sys
from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

main_py_code = """from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {context_variables}

if __name__ == "__main__":
    run_demo_loop({starting_agent}, context_variables=context_variables, stream=True, debug=True)"""

# MANAGER TOOLS
# Function to create the agency structure
def create_swarm_structure(context_variables: Dict, starting_agent: Agent) -> str:
    """
    This function creates the necessary directories and files for the specified swarm, including
    `configs` and `data` folders. It also generates the `main.py` file and other initialization files.
    """
    try:
        swarm_name = context_variables.get("swarm_name")
    except Exception as e:
        return "Please `update_context_variables_manager` before trying to `update_goals`"

    os.makedirs(f'inceptions/{swarm_name}/configs', exist_ok=True)
    os.makedirs(f'inceptions/{swarm_name}/configs', exist_ok=True)
    os.makedirs(f'inceptions/{swarm_name}/data', exist_ok=True)
    
    with open(f'inceptions/{swarm_name}/__init__.py', 'w') as f:
        f.write('# Init file for swarm\n')
    with open(f'inceptions/{swarm_name}/configs/__init__.py', 'w') as f:
        f.write('# Init file for configs\n')
    with open(f'inceptions/{swarm_name}/data/__init__.py', 'w') as f:
        f.write('# Init file for data\n')

    with open(f'inceptions/{swarm_name}/data/__init__.py', 'w') as f:
        f.write('# Init file for data\n')

    with open(f'inceptions/{swarm_name}/configs/agents.py', 'w') as f:
        f.write('# Agents configuration file\n\n')

    with open(f'inceptions/{swarm_name}/configs/tools.py', 'w') as f:
        f.write('# Tools configuration file\n\n')

    with open(f'inceptions/{swarm_name}/main.py', 'w') as f:
        f.write(main_py_code.format(
            context_variables=context_variables,
            starting_agent=starting_agent,
            ))

    return "Swarm Directory has been successfully created. Move on to create the required agents and tools within the generated folders."



def update_goals(context_variables: Dict, goals: str) -> str:
    """
    This function writes the specified goals and mission statement to the `goals.md` file located
    in the `data` directory of the swarm.
    """
    try:
        swarm_name = context_variables.get("swarm_name")
    except Exception as e:
        return "Please `update_context_variables_manager` before trying to `update_goals`"
    
    try:
        with open(f'inceptions/{swarm_name}/data/goals.md', 'w') as f:
            f.write(goals)
    except Exception as e:
        return "Please `create_swarm_structure` before setting goals."
    
    context_variables.update(
        {
            "swarm_goals": goals,
        }
    )

    return "Goals and Mission for the swarm has been updated."


def update_context_variables_manager(context_variables: Dict, swarm_name: str, swarm_structure: List[Union[str, List]]):
    context_variables.update(
        {
            "swarm_name": swarm_name,
            "swarm_structure": swarm_structure
        }
    )
    print('Context Variables:\n', context_variables)

    return "Swarm Name and Structure have been successfully updated."


# AGENT CREATOR TOOLS
agent_imports = """from configs.tools import *
from swarm import Agent"""

agent_template = """{agent_imports}

def {agent_name}_instructions():
    return \"\"\"{instructions}\"\"\"

{transfer_functions}

{agent_name} = Agent(
    name="{agent_name}",
    instructions={agent_name}_instructions(),
    functions=[{functions}],
)
"""

def update_context_variables_agentcreator(context_variables: Dict, agent_tools: Dict):

    context_variables.update(
        {
            "agent_tools": agent_tools
        }
    )
    print('Context Variables:\n', context_variables)

    return "Context variables have been successfully updated with agent_tools."


def create_transfer_function(transfer_agent):
    """
    Generates a transfer function for an agent to transfer control.
    """
    return f"""
def transfer_to_{transfer_agent}():
    return {transfer_agent}
"""

def create_agents(context_variables: Dict) -> str:
    """
    This function constructs the code for all agents, including instructions, transfer functions,
    and any additional specified functions. It writes the generated code to `agents.py`.
    """
    swarm_name = context_variables.get('swarm_name')
    swarm_structure = list(context_variables.get('swarm_structure'))

    # agent_tools = json.loads(context_variables.get('agent_tools'))
    agent_tools = context_variables.get('agent_tools').replace("'", '"')
    try:
        agent_tools = json.loads(agent_tools)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    # Initialize the path for the agents.py file
    agents_file_path = os.path.join(f'inceptions/{swarm_name}/configs', 'agents.py')

    # Loop through each agent in the swarm structure
    for i, (agent_name, agent_info) in enumerate(agent_tools.items()):
        tools = list(agent_info['tools'])
        agent_instructions = agent_info['agent_instructions']

        # Find transfer agents based on the swarm structure
        transfer_agents = []
        for connection in swarm_structure:
            if isinstance(connection, list) and connection[0] == agent_name:
                transfer_agents.append(connection[1])

        # Create transfer functions for this agent
        transfer_functions = "\n".join([create_transfer_function(agent) for agent in transfer_agents])
        
        # List of transfer functions and additional functions/tools
        all_functions = [f"transfer_to_{agent}" for agent in transfer_agents]
        all_functions.extend(tools)

        # Join functions for the template
        functions_str = ", ".join(all_functions)

        # Format the agent code using the template
        if i==0:
            agent_code = agent_template.format(
                agent_imports=agent_imports,
                agent_name=agent_name,
                instructions=agent_instructions,
                transfer_functions=transfer_functions,
                functions=functions_str
            )
        else:
                agent_code = agent_template.format(
                agent_imports="",
                agent_name=agent_name,
                instructions=agent_instructions,
                transfer_functions=transfer_functions,
                functions=functions_str
            )
        
        # Write the agent code to the agents.py file
        with open(agents_file_path, "a") as f:
            f.write("\n\n" + agent_code)

    return f"All agents for the swarm '{swarm_name}' have been successfully created."



# TOOL CREATOR TOOLS
# Template for creating new tools
tool_template = """{imports}

{tool_code}
"""

def create_tool(context_variables: Dict, tool_name: str, tool_code: str, tool_imports: List) -> str:
    """
    Generates a new tool based on the provided parameters and writes it to the tools.py file.

    Args:
    tool_name (str): The name of the tool to be created.
    tool_code (str): Python class implementation of the tool to be added to the 'tools.py' file.
    tool_imports (List)): The necessary import statements for the tool as a List ['import numpy as np', 'import pandas as pd',]
    """

    def is_function_code(code: str) -> bool:
        """
        Validates if the given code string is a function and not a class.
        """
        try:
            parsed_code = ast.parse(code)  # Parse the code into an AST (Abstract Syntax Tree)
            for node in parsed_code.body:
                if isinstance(node, ast.FunctionDef):
                    return True
                if isinstance(node, ast.ClassDef):
                    return False
        except SyntaxError:
            return False
        return False
    
    # Validate if the provided tool_code is a function
    if not is_function_code(tool_code):
        return "Error: The provided tool_code is a class, but only functions are allowed."
    
    print(f"Creating a tool for: {tool_name}")
    swarm_name = context_variables.get("swarm_name")
    agent_tools = json.loads(context_variables.get('agent_tools'))
    print(agent_tools)

    path = f'inceptions/{swarm_name}/configs/'
    os.makedirs(path, exist_ok=True)  # Ensure the directory exists
    tools_file_path = os.path.join(path, "tools.py")

    if isinstance(tool_imports, str):
        tool_imports = tool_imports.split(",")

    for imp in tool_imports:
        if is_import_in_tools_file(tools_file_path, imp):
            pass
        else:
            add_import_to_tools_file(tools_file_path, imp)

    # Write the tool code to the tools.py file, appending if it exists
    mode = "a" if os.path.exists(tools_file_path) else "w"
    with open(tools_file_path, mode) as f:
        f.write("\n\n" + tool_code)

    return f"{tool_name} has been successfully created."


# Google Custom Search API setup
API_KEY = "AIzaSyAFgqauNFcsyn5_BmfHzk3VpZ4mXOsHGQU"
SEARCH_ENGINE_ID = "04d381c3e293144a2"

def web_search(query, question):
    """
    Perform a Google Custom Search to find API documentation or find any relevant data and scrape the first URL for relevant information.
    """

    search_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "q": query,
        "num": 1 
    }
    
    response = requests.get(search_url, params=params)
    search_results = response.json()

    first_url = search_results["items"][0]["link"]

    page_response = requests.get(first_url)
    soup = BeautifulSoup(page_response.content, 'html.parser')
    page_text = soup.get_text(separator=' ', strip=True)

    extracted_info = query_gpt_for_information(page_text, question)

    return extracted_info


def query_gpt_for_information(content, question):
    """
    Send the scraped content to GPT or another LLM to extract relevant information.

    Args:
    content (str): The full scraped content.
    question (str): The question to ask (e.g., "What is the base URL?").

    Returns:
    str: The relevant answer extracted by the LLM.
    """

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": f"Based on the following documentation, {question}\n\n{content}"
        }
    ]
)
    
    return response.choices[0].message.content

def load_tools_module(tools_file_path):
    """
    Dynamically loads the tools.py file as a module.
    """
    spec = importlib.util.spec_from_file_location("tools", tools_file_path)
    tools_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tools_module)
    return tools_module

def is_import_in_tools_file(tools_file_path, import_name):
    """
    Check if a particular import statement exists in the tools.py file.
    """
    with open(tools_file_path, "r") as file:
        content = file.read()
        return f"import {import_name}" in content or f"from {import_name}" in content
    
def add_import_to_tools_file(tools_file_path, import_statement):
    """
    Adds a required import statement to the beginning of the tools.py file.
    """
    with open(tools_file_path, "r") as file:
        content = file.readlines()
    
    # Prepend the new import statement to the beginning of the content
    content.insert(0, f"{import_statement}\n")
    
    with open(tools_file_path, "w") as file:
        file.writelines(content)

def check_and_install_imports(required_imports, tools_file_path):
    """
    Check for missing imports and install them if necessary.
    """
    for imp in required_imports:
        module_name = imp.split()[-1]  # Extract the module name (e.g., "pandas" from "import pandas")
        
        if not is_import_in_tools_file(tools_file_path, module_name):
            add_import_to_tools_file(tools_file_path, imp)
        try:
            importlib.import_module(module_name)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', module_name])
                importlib.import_module(module_name)
            except ImportError:
                print(f"Error: Could not install the required import '{module_name}'")

    
def extract_imports_from_function(tool_code):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful code reviewer"},
        {
            "role": "user",
            "content": f"""Based on the following code snippet for a python function:
Tool Code
---------------------       
{tool_code}

Return a python list of all the imports required by the method.

For example;
Tool Code:
---------------------
def my_function():
    data = pd.DataFrame(np.random.randn(100, 4))
    model = LinearRegression()
    model.fit(data.iloc[:, :-1], data.iloc[:, -1])
    return model
    
The return
["import pandas as pd", "from sklearn.linear_model import LinearRegression"]

Only return the python list."""
        }
    ]
)
    
    return response.choices[0].message.content



def validate_tool(context_variables, tool_name, tool_testing_arguments: dict):
    """
    Validates a tool by importing and running the tool function.
    
    Args:
        context_variables (dict): Context info (like swarm_name).
        tool_name (str): The name of the tool to validate.
        tool_testing_arguments (dict): Arguments to pass to the tool function when running.

    Returns:
        str: Validation results with success or error messages.
    """
    swarm_name = context_variables.get("swarm_name")
    path = f'inceptions/{swarm_name}/configs/'
    tools_file_path = os.path.join(path, "tools.py")
    
    errors = ""
    
    if not os.path.exists(tools_file_path):
        return "Error: tools.py file does not exist. First create tools."
    
    try:
        tools_module = load_tools_module(tools_file_path)
    except Exception as e:
        return f"Error: Failed to load tools.py. Exception: {str(e)}"
    
    if not hasattr(tools_module, tool_name):
        return f"Error: Tool '{tool_name}' not found in tools.py. First create the tool and then validate it."
    
    tool_function = getattr(tools_module, tool_name)
    
    required_imports = extract_imports_from_function(tool_function)
    check_and_install_imports(required_imports)
    
    try:
        tool_function(**tool_testing_arguments)
    except Exception as e:
        errors += f"Error: Tool '{tool_name}' encountered error: {str(e)}"
    
    if errors:
        return f"Errors encountered:\n{errors}\n\nTool '{tool_name}' validated with the above errors."
    
    return f"Tool '{tool_name}' validated successfully."

