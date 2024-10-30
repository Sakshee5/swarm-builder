# TO-DO
- Read up on function calling!
1. Tools are currently being created as classes sometimes. Ensure they are always created as functions.
15. if you cant build the tool (cant write code), give instructions on how it can be possibly built or what the challenges are


- create_tool is creating erroneous functions
- validate_tool testing parameters need to be GPT generated.
- can ask system to generate GPT tools

2. Add evals for swarm builder
3. Configure swarm builder to build evals
4. Test complex workflows - multiple agents and tools
5. Rethink directory structure? (if needed)
6. Use context_variables like user_name to make it more personalized
7. streamlit app should have a login page and then a chatbot
8. Have new swarm as streamlit?
9. Tools to validate tool creation/agent creation. For example, check imports, if api_key is required then ask user to provide/guide how to get it/set it later.
10. Refine Prompts to ensure minimum token usage. Are instructions being repeated?
11. Use swarm goals?
12. Find and Reduce temperature.
13. Imports are being added seperately for each tool. Shift them at the top of the file.
14. swarm iteration


Since OpenAI just released the Swarm framework, we saw an opportunity to explore its potential. Initially, we had a variety of ideas, from personalized newsletters to study strategy assistants for college students. But then we thought—why limit ourselves to one use case? What if we could build a meta-swarm that could dynamically generate any type of swarm you need, based on natural language input? This idea pushes the boundaries of multi-agent systems by enabling users to define their problem, and our meta-swarm takes care of the rest—creating a personalized, highly efficient swarm of agents tailored to the task, whether it’s for time management, content curation, or even business automation.

From a technical perspective, weve combined LLM capabilities with iterative techniques to ensure each swarm is optimized for the users goals. This system not only builds swarms but continuously improves them.
What makes our project stand out is the novelty of the meta-swarm approach. Instead of building agents for one specific problem, weve built a framework that generates agents for any problem. This flexibility opens up new possibilities for generating quick drafts for any 
In terms of commercial viability, it can be platform where users can subscribe to generate custom AI swarms to automate their workflows, reduce costs, and increase efficiency.