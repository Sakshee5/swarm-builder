from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'YouTubeVideoPromotion', 'swarm_structure': '["manager", ["manager", "youtube_data"], ["youtube_data", "content_creator"], ["content_creator", "manager"]]'}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)