import os
import json
from swarm import Agent
from typing import List, Dict, Union, Any

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

    os.makedirs(f'examples/{swarm_name}/configs', exist_ok=True)
    os.makedirs(f'examples/{swarm_name}/data', exist_ok=True)
    
    with open(f'examples/{swarm_name}/__init__.py', 'w') as f:
        f.write('# Init file for swarm\n')
    with open(f'examples/{swarm_name}/configs/__init__.py', 'w') as f:
        f.write('# Init file for configs\n')
    with open(f'examples/{swarm_name}/data/__init__.py', 'w') as f:
        f.write('# Init file for data\n')

    with open(f'examples/{swarm_name}/main.py', 'w') as f:
        f.write(main_py_code.format(
            context_variables=context_variables,
            starting_agent=starting_agent,
            ))

    return "Swarm Structure has been successfully created."



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
        with open(f'examples/{swarm_name}/data/goals.md', 'w') as f:
            f.write(goals)
    except Exception as e:
        return "Please `create_swarm_structure` before setting goals."

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

AgentType = Dict[str, Union[
    List[str],  # List of tools or tool descriptions
    str         # Agent instructions
]]

JsonType = Dict[str, AgentType]

def update_context_variables_agentcreator(context_variables: Dict, agent_tools: Any):
    try:
        _ = json.loads(agent_tools)

        context_variables.update(
        { 
            "agent_tools": agent_tools
        }
    )

        print('Context Variables:\n', context_variables)
        return "Context variables have been successfully updated with agent_tools."

    except:
        return "agent_tools should be a valid JSON."


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
    agent_tools = json.loads(context_variables.get('agent_tools'))

    # Initialize the path for the agents.py file
    agents_file_path = os.path.join(f'examples/{swarm_name}/configs', 'agents.py')

    # Create or clear the agents.py file
    with open(agents_file_path, "w") as f:
        f.write("# Agents configuration file\n\n")

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

def {tool_name}():
    \"\"\"
    {tool_description}
    \"\"\"
    {tool_code}
"""

def create_tool(context_variables: Dict, tool_name: str, tool_code: str, tool_imports: str) -> str:
    """
    Generates a new tool based on the provided parameters and writes it to the tools.py file.

    Args:
    tool_name (str): The name of the tool to be created.
    tool_code (str): Python class implementation of the tool to be added to the 'tools.py' file.
    tool_imports (str): The necessary import statements for the tool.
    """
    swarm_name = context_variables.get("swarm_name")
    agent_tools = json.loads(context_variables.get('agent_tools'))

    tool_description = None

    # Find the tool description based on the tool_name
    for agent_name, agent_info in agent_tools.items():
        if tool_name in agent_info['tools']:
            idx = agent_info['tools'].index(tool_name)
            tool_description = agent_info['tool_descriptions'][idx]
            break

    # Check if the tool was found
    if not tool_description:
        return f"Tool description for {tool_name} not found."

    path = f'examples/{swarm_name}/configs/'
    os.makedirs(path, exist_ok=True)  # Ensure the directory exists
    tools_file_path = os.path.join(path, "tools.py")

    # Format the tool code using the template
    tool_code_str = tool_template.format(
        imports=tool_imports,
        tool_name=tool_name,
        tool_description=tool_description,
        tool_code=tool_code
    )

    # Write the tool code to the tools.py file, appending if it exists
    mode = "a" if os.path.exists(tools_file_path) else "w"
    with open(tools_file_path, mode) as f:
        f.write("\n\n" + tool_code_str)

    return f"{tool_name} for {agent_name} has been successfully created."
