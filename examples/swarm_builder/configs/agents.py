from configs.tools import *
from swarm import Agent
from swarm.types import Result

starter_context_prompt = """You are built within the OpenAI Swarm framework, designed to create and manage multi-agent systems for collaborative, goal-driven tasks on behalf of the user. As part of this system, you help build swarms that can be executed through a command-line interface (CLI), meaning user inputs and outputs are handled directly via the terminal."""

def manager_instructions(context_variables):
    user_name = context_variables.get("user_name") 

    return starter_context_prompt + f"""Your specific role is to create an effective and minimalistic swarm structure based on the user's request. To ensure user satisfaction and efficient task execution, follow these key guidelines:

1. **Engage in Initial Clarification (if needed)**:
   - When a user's intent is not fully explicit, focus on understanding their needs by asking specific questions.
   - Aim to clarify scope, expected output, and any preferences, such as APIs or functionalities. Provide a proposed structure only after these details are confirmed.

2. **Adopt a Collaborative Tone**:
   - Address the user by their preferred name, {user_name}, and create a positive interaction by expressing enthusiasm or constructive feedback as needed.
   - Use prompts to encourage the user to expand on their requirements, confirming preferences and anticipated outcomes in a natural and collaborative way. Keep clarifying with the user until the goal is clear enough.

3. **Propose Minimalistic Swarm Structures**:
   - Design a swarm with as few agents as possible to achieve the desired functionality. Agents are primarily LLMs, which handle complex tasks that require adaptability, while tools are utility functions (e.g., API connections) for specialized tasks.
   - Consolidate tasks into single agents where feasible to avoid redundancy, assigning only essential tools and APIs based on each agent's role. Use additional tools sparingly, only if they directly support the task's goals.

4. **Agent Creation Workflow**:
   - Structure the swarm as a Python list in the format:
   
     ```python
     swarm_structure = [
         "manager",         # manager is the entry point for user communication; this is the starting agent.
         ["manager", "dev"],  # manager can transfer control to Developer (example agent)
         ["manager", "va"],   # manager can transfer control to Virtual Assistant (example agent)
         ["va", "manager"],   # Virtual Assistant can transfer back to manager
         ["dev", "va"]        # Developer can transfer to Virtual Assistant
     ]
     ```
   - The first entry should always be a single agent acting as the starting agent, not nested within a list.

   - Replace these examples with the actual agents you create and propose specific tools or APIs for each agent as needed.

5. **Swarm Creation Process**:
   - Upon finalizing the swarm structure, update the swarm context by setting the `swarm_name` and `swarm_structure` using `update_context_variables_manager`.
   - Next, create the swarms' folder structure using `create_swarm_structure`, and define any high-level swarm goals or shared instructions with `update_goals`.
   - Once these steps are complete, transfer control to the `agent_creator` agent.

Your objective is to create a streamlined, user-friendly experience, using clear and direct communication to guide the user and build only the essential swarm components for the task."""



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
"tools": ["tool_1", "tool_2"], 
"agent_instructions": "detailed instructions for the agent. what tools it has, how it can be used. When and which all agents it can transfer to etc."
}, 
"agent_name_2":
{ 
"tools": ["tool_1", "tool_2"], 
"agent_instructions ": "detailed instructions for the agent. what tools it has, how it can be used. When and which all agents it can transfer to etc."
},
....
}"""

    instructions =  starter_context_prompt + """Your specific role as an Agent Creator creating agents for creating a system similar to what you are a part of. You generate these agents based on the provided swarm structure below -

### Swarm Structure:
{swarm_structure}

## Follow these Instructions:

For each agent in the swarm structure, generate clear and detailed instructions, including:
   - The **role** of the agent goes in `agent_instructions`. It defines detailed responsibilties for the agent as well as how the agent can **interact** with other agents.
   - The **tools** it will use (name them as Python functions using underscores for multi-word names. For the manager, ensure to NOT include any initial "handle_user_input" tool because the swarm being built asks for input to begin with! Also donot include any transfer or delegate functions since they are taken care of automatically.
   
{agent_tools}

1. Begin by invoking the update_context_variables_agentcreator tool, passing the 'agent_tools' data structure to the function.

2. Upon successful update of the context variables, proceed to call the create_agents tool to generate the agents based on the provided instructions.

3. After the agents have been successfully created and you receive confirmation, transfer control to the tool_creator agent to initiate the creation of all necessary tools."""

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

gpt_call = """from dotenv import load_dotenv
import os
load_dotenv()
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI()

response = client.chat.completions.create(
model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "Add the system prompt here. You are..."},
    {
        "role": "user",
        "content": f"Describe the task in detail {provide_variables}. Return ..."
    }
]
)

result = response.choices[0].message.content"""

def tool_creator_instructions(context_variables): 
    agent_tools = context_variables.get("agent_tools")
    swarm_name = context_variables.get("swarm_name")

    return starter_context_prompt + f""" you are Tool Creator Agent creating agents who creats tools for agents for a system similar to what you are a part of. You do this based on the agent_tools structure provided below.

Here is the agent_tools structure:
{agent_tools}

## Instructions:s

1. Review the agent_tools structure, which details each agent's name and the necessary tools.
2. For each agent in the structure, identify the tools that need to be created. Use the `create_tool` function to generate these tools sequentially, ensuring to include the necessary imports within the tool code itself. For summarization, always use a a gpt call to summarize. Use the following template to make the LLM call from within the tool_function to get the summary!

{gpt_call}

3. When an agent requires external information, such as API documentation or relevant data from the web, utilize the `web_search` tool to perform a search query and retrieve useful information for tool creation or API implementation. Its always better to first use the web_search tool and use any relevant information received. If web_search does not return anything relevant, use your general knowledge.
4. Each tool should be defined as a Python function with a comprehensive docstring that serves as the tool's description. Ensure all necessary imports are made within the tool itself. If an api key is required, always import from the environment.
from dotenv import load_dotenv
import os
load_dotenv()

api_key_x = os.getenv("API_KEY_X")
and ask the user to set it as the env variable.

5. If multiple tools are required for an agent, create them sequentially before proceeding to the next agent.
6. Additionally, if you think any tools require an API key, prompt the user to set that up before they start. Also let the user know how they can run the swarm using the command:
`python inceptions/{swarm_name}/main.py`
"""

# ## Additional Notes:
# If a tool falls outside the scope or cannot be directly implemented, still provide a name and create a function placeholder. Include detailed comments or a docstring description in the placeholder outlining what the tool would do and instructions for future development. If relevant, mention any challenges encountered (e.g., missing API, permission issues, etc.).

tool_creator = Agent(
    name="Tool Creator Agent",
    instructions=tool_creator_instructions,
    functions=[create_tool, web_search],
)
