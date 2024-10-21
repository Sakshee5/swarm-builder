from configs.tools import *
from swarm import Agent
from swarm.types import Result

def manager_instructions(context_variables):
   user_name = context_variables.get("user_name") 

   return f"""As a Manager Agent within the OpenAI Swarm framework, your mission is to help users define the simplest and most effective structure of their agent-swarm based on their specific requirements. The user you are addressing is: {user_name}

1. Understand the user's intent and determine the simplest swarm structure that meets their goals directly. Avoid adding unnecessary agents unless they provide a clear benefit or optimization.
2. Propose the initial swarm name, structure, agent names, and roles. The agent names must be tailored for the purpose of the agency. Make sure to confirm this information with the user before proceeding. The structure should include:
    - The name of the swarm.
    - All agents with clear and concise roles.
    - Any essential tools/APIs each agent will require.

You should structure it in the following way:
swarm_structure = [
    manager          # manager is the entry point for communication with user. This is the starting agent.
    [manager, dev],  # manager can transfer to Developer (sample agent)
    [manager, va],   # manager can transfer to Virtual Assistant (sample agent)
    [va, manager],   # Virtual Assistant can transfer back to the manager
    [dev, va]        # Developer can transfer to Virtual Assistant
]

First entry should always be a single agent which will act as the starting agent. It should not be in a list.

Keep in mind that this is just an example and you should replace it with the actual agents you are creating. Also, propose which tools or APIs each agent should have access to, if any with a brief description of each role. Then, after the user's confirmation, send each agent to the `agent_creator` one by one, starting with the first one which is manager in this case.

4. Use `update_context_variables_manager` to update the swarm_name and swarm_structure.
5. Use `create_swarm_structure` to create a folder structure for the swarm.
6. Use `update_goals` to set the swarm's goals/mission/shared instructions.
7. Transfer control to `agent_creator` to create these agents one by one based on the confirmed structure."""

def transfer_to_agent_creator(context_variables: dict):
    """Transfers control to Agent Creator and Updates the context variables with name of the swarm chosen."""
    
    return Result(
       value="Done",
       agent=agent_creator,
       context_variables = context_variables
   )

manager_agent = Agent(
    name="Manager Agent",
    instructions=manager_instructions,
    functions=[create_swarm_structure, update_context_variables_manager, update_goals, transfer_to_agent_creator],
)


def agent_creator_instructions(context_variables):
    swarm_structure = context_variables.get("swarm_structure")

    agent_tools = """[ 
        { 
            "agent_name": "agent_name_1", 
            "tools": ["tool1", "tool2"], 
            "tool_descriptions": 
            { 
                "tool1": "Description for tool1", 
                "tool2": "Description for tool2",
                ...
            },
            "agent_instructions": "detailed instructions for the agent. what tools it has, how it can be used. When and which all agents it can transfer to etc."
        }, 
        { 
            "agent_name": "agent_name_1", 
            "tools": ["tool1", "tool2"], 
            "tool_descriptions": 
            { 
                "tool1": "Description for tool1", 
                "tool2": "Description for tool2",
                ...
            } ,
            "agent_instructions": "detailed instructions for the agent. what tools it has, how it can be used. When and which all agents it can transfer to etc."
        },
        ....
    ]"""

    instructions =  """You are an agent responsible for creating other agents based on the provided swarm structure. Follow these instructions to create each agent and define the tools they will need.

### Swarm Structure:
{swarm_structure}

## Primary Instructions:

1. **Analyze Each Agent's Role**:
   - Review the role of each agent based on the swarm structure and the users goals. For instance, if an agent is a `data_fetcher`, identify the APIs or tools it will need for fetching and processing external data relevant to the swarm's purpose.

2. **Define the Tools and Descriptions**:
   - Based on your analysis, come up with a structure that defines the tools and APIs required for each agent in the format below:
   
{agent_tools}

- Make sure each tool or API aligns with the agents role and its functions within the swarm.

3. Use the `update_context_variables_agentcreator` to update the `context_variables`.

4. Use the `create_agents` tool to generate the agents based on the `agent_and_tools` structure.

6. Once the agents are created, transfer control to the `tool_creator` agent for it to create all the required tools.
"""

    return instructions.format(
        swarm_structure = swarm_structure,
        agent_tools = agent_tools
        )

def transfer_to_tool_creator(context_variables: dict):
    return Result(
       value="Done",
       agent=tool_creator,
       context_variables = context_variables
   )

agent_creator = Agent(
    name="Agent Creator Agent",
    instructions=agent_creator_instructions,
    functions=[update_context_variables_agentcreator, create_agents, transfer_to_tool_creator],
)

def tool_creator_instructions(context_variables):
    agent_tools = context_variables.get("agent_tools")

    return f"""As a Tool Creator Agent within the Swarm framework, your role is to create tools for each agent as defined in the agent_tools structure.

Here is the agent_tools structure:
{agent_tools}

## Instructions:

1. Review the agent_tools structure, which includes details about each agent's name, the tools they need, and their descriptions.
2. For each agent in the list, identify all tools that need to be created. Use the `create_tool` function to generate these tools. Ensure you accurately implement real-world APIs or SDKs when creating the tools.
3. If multiple tools are required for an agent, create them sequentially before moving on to the next agent.
4. Once all tools for all agents have been created, update the user that the swarm has been created.
"""

tool_creator = Agent(
    name="Tool Creator Agent",
    instructions=tool_creator_instructions,
    functions=[create_tool],
)
