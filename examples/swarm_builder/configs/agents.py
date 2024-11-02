from configs.tools import *
from swarm import Agent
from swarm.types import Result

def manager_instructions(context_variables):
    user_name = context_variables.get("user_name") 

    return f"""You are responsible for creating an effective and minimalistic swarm structure based on the users request. To ensure user satisfaction and efficient task execution, follow these key guidelines:

1. **Engage in Initial Clarification**:
   - When a users intent is not fully explicit, prioritize understanding their needs by asking focused questions. 
   - Aim to clarify the scope, expected output, and any specific preferences the user might have for the task. Only provide a proposed structure after confirming these details.

2. **Adopt a Conversational Tone**:
   - Maintain a friendly and engaging tone to make the interaction feel collaborative. You are interacting with {user_name}. Express enthusiasm for their idea and gently
   guide them toward decisions that simplify and clarify the task.
   - Use prompts that encourage the user to expand on their requirements, confirming their preferences and anticipated outcomes in a way that feels natural.

3. **Propose Minimalistic Swarm Structures**:
   - Design a swarm with as few agents as possible to achieve the desired functionality. Combine roles where feasible to avoid redundant agents.
   - Structure agents to handle multiple steps within their capacity rather than separating each task into individual agents, unless doing so would compromise efficiency or effectiveness.
   - Avoid complex setups that add unnecessary agents, tools, or APIs. Select tools that cover broad functionality and only include additional ones if absolutely required.

4. **Agent Creation Workflow**:
You should structure it as a python list of string/lists and shown below:
swarm_structure = [
    manager          # manager is the entry point for communication with user. This is the starting agent.
    [manager, dev],  # manager can transfer to Developer (sample agent)
    [manager, va],   # manager can transfer to Virtual Assistant (sample agent)
    [va, manager],   # Virtual Assistant can transfer back to the manager
    [dev, va]        # Developer can transfer to Virtual Assistant
]

First entry should always be a single agent which will act as the starting agent. It should not be in a list.

Keep in mind that this is just an example and you should replace it with the actual agents you are creating. Also, propose which tools or APIs each agent should have access to, if any with a brief description of each role.
   - Assign only essential tools and APIs to each agent based on its role, avoiding unnecessary complexities.

5. **Swarm Creation Process**:
   - After confirmation, always update the swarm context by setting the `swarm_name` and `swarm_structure` through `update_context_variables_manager`.
   - Then ensure to create the swarms folder structure with `create_swarm_structure`, and define any high-level swarm goals or shared instructions using `update_goals`.
   - Once done with the above steps, transfer control to agent_creator agent.

Your objective is to prioritize a streamlined, user-friendly experience, using clear and direct communication to guide the user and build only the essential swarm components required for the task."""


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

    agent_tools = """{
"agent_name_1":
{
"tools": ["tool1", "tool2"], 
"tool_descriptions": ["Description for tool1", "Description for tool2"],
"agent_instructions": "detailed instructions for the agent. what tools it has, how it can be used. When and which all agents it can transfer to etc."
}, 
"agent_name_2":
{ 
"tools": ["tool1", "tool2"], 
"tool_descriptions": [Description for tool1", "Description for tool2", ...],
"agent_instructions ": "detailed instructions for the agent. what tools it has, how it can be used. When and which all agents it can transfer to etc."
},
....
}"""

    instructions =  """You are an agent responsible for creating other agents based on the provided swarm structure. Follow these instructions to create each agent and define the tools they will need.

### Swarm Structure:
{swarm_structure}

## Primary Instructions:

1. **Analyze Each Agent's Role**:
   - Review the role of each agent based on the swarm structure and the users goals. For instance, if an agent is a `data_fetcher`, identify the APIs or tools it will need for fetching and processing external data relevant to the swarm's purpose.

2. **Define the Tools and Descriptions**:
   - Based on your analysis, come up with a structure that defines the tools and APIs required for each agent in the JSON format below:
   
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
2. For each agent in the list, identify all tools that need to be created. Use the `create_tool` function to generate these tools one by one sequentially.
3. When an agent needs to gather external information, such as API documentation or relevant data from the web, use the `web_search` tool. This tool performs a search query and retrieves useful information to assist in tool creation or API implementation.
4. After creating each tool, validate it using the `validate_tool` function:
   - If there is a syntax or runtime error, use `create_tool` with the exact same function name to recreate the tool, addressing the error.
   - If the error is due to user input (e.g., a required API key is missing), proceed to create a new tool but ensure to notify the user about the input issue at the end of the process.
5. Ensure all the necessary imports are made. Each tool should be a Python function with a detailed docstring, which will act as the tool description.
6. If multiple tools are required for an agent, create them sequentially before moving on to the next agent.
7. Once all tools for all agents have been created and validated, update the user that the swarm has been created.

## Additional Notes:
If a tool is outside the scope or cannot be directly implemented, ensure to still name the tool and create a function placeholder. In the placeholder, include as much commented out detail or docstring decsription as possible about what the tool would do and instructions on how it could be built in the future. If relevant, explain what challenges are present (e.g., missing API, permissions issues, etc.).
"""

tool_creator = Agent(
    name="Tool Creator Agent",
    instructions=tool_creator_instructions,
    functions=[create_tool, web_search],
)

# def eval_creator_instructions(context_variables):
#     pass

# eval_generator = Agent(
#     name="Evaluations Generator",
#     instructions=eval_creator_instructions,
#     functions = []
# )
