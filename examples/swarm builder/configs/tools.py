import os

main_py_code = """from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {}

if __name__ == "__main__":
    run_demo_loop(triage_agent, context_variables=context_variables, debug=True)"""

# MANAGER TOOLS
# Function to create the agency structure
def create_swarm_structure(swarm_name: str) -> str:
    """
    This function creates the necessary directories and files for the specified swarm, including
    `configs` and `data` folders. It also generates the `main.py` file and other initialization files.
    """
    os.makedirs(f'examples/{swarm_name}/configs', exist_ok=True)
    os.makedirs(f'examples/{swarm_name}/data', exist_ok=True)
    
    with open(f'examples/{swarm_name}/__init__.py', 'w') as f:
        f.write('# Init file for swarm\n')
    with open(f'examples/{swarm_name}/configs/__init__.py', 'w') as f:
        f.write('# Init file for configs\n')
    with open(f'examples/{swarm_name}/data/__init__.py', 'w') as f:
        f.write('# Init file for data\n')

    with open(f'examples/{swarm_name}/main.py', 'w') as f:
        f.write(main_py_code)

    with open(f'examples/{swarm_name}/data/prompts.py', 'w') as f:
        f.write("")

    return "Swarm Structure has been successfully created."



def update_goals(swarm_name: str, goals: str) -> str:
    """
    This function writes the specified goals and mission statement to the `goals.md` file located
    in the `data` directory of the swarm.
    """
    with open(f'examples/{swarm_name}/data/goals.md', 'w') as f:
        f.write(goals)

    return "Goals and Mission for the swarm has been updated."


# AGENT CREATOR TOOLS
agent_template = """from configs.tools import *
from swarm import Agent

def {agent_name}_instructions():
    return \"\"\"{instructions}\"\"\"

{transfer_functions}

{agent_name} = Agent(
    name="{agent_name}",
    instructions={agent_name}_instructions(),
    functions=[{functions}],
)
"""

def create_transfer_function(transfer_agent):
    """
    Generates a transfer function for an agent to transfer control.
    """
    return f"""
def transfer_to_{transfer_agent}():
    return {transfer_agent}
"""

def create_agent_template(
    swarm_name: str, 
    agent_name: str, 
    instructions: str, 
    transfer_agents: list[str] = [], 
    additional_functions: list[str] = None
) -> str:
    """
    This function constructs the code for an agent, including instructions, transfer functions,
    and any additional specified functions. It writes the generated code to `agents.py`.
    """
    transfer_functions = "\n".join([create_transfer_function(agent) for agent in transfer_agents])
    
    # List of transfer functions and additional functions/tools
    all_functions = [f"transfer_to_{agent}" for agent in transfer_agents]
    if additional_functions:
        all_functions.extend(additional_functions)
        
    # Join functions for the template
    functions_str = ", ".join(all_functions)

    # Format the agent code using the template
    agent_code = agent_template.format(
        agent_name=agent_name,
        instructions=instructions,
        transfer_functions=transfer_functions,
        functions=functions_str
    )
    agents_file_path = os.path.join(f'examples/{swarm_name}/configs', 'agents.py')
    
    # Check if the agents.py file exists and append or create it
    if os.path.exists(agents_file_path):
        with open(agents_file_path, "a") as f:
            f.write("\n\n" + agent_code)
    else:
        with open(agents_file_path, "w") as f:
            f.write(agent_code)

    return f"{agent_name} for the swarm {swarm_name} has been successfully created."



# TOOL CREATOR TOOLS
# Template for creating new tools
tool_template = """def {tool_name}():
    \"\"\"
    {tool_description}
    \"\"\"
    {tool_code}
"""


def create_tool(swarm_name: str, tool_name: str, tool_description: str, tool_code: str) -> str:
    """
    Generates a new tool based on the provided parameters and writes it to the tools.py file.
    """
    # Format the tool code using the template
    tool_code_str = tool_template.format(
        tool_name=tool_name,
        tool_description=tool_description,
        tool_code=tool_code
    )

    # Define the path to the tools file
    path = f'examples/{swarm_name}/configs/'
    os.makedirs(path, exist_ok=True)  # Ensure the directory exists

    tools_file_path = os.path.join(path, "tools.py")

    # Check if the tools.py file exists and append or create it
    if os.path.exists(tools_file_path):
        with open(tools_file_path, "a") as f:
            f.write("\n\n" + tool_code_str)
    else:
        with open(tools_file_path, "w") as f:
            f.write(tool_code_str)

    return f"{tool_name} has been successfully created."
