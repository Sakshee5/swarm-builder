from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'TwitchLiveChecker', 'swarm_structure': '["manager", ["manager", "live_status_checker"], ["live_status_checker", "manager"], ["live_status_checker", "humor_messenger"]]', 'swarm_goals': '1. Check if a specified Twitch streamer is currently live using the Twitch API.\n2. If the streamer is not live, send the user a funny message to lighten the mood.\n3. Ensure seamless interaction between the user and the agents for accurate and timely updates.'}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)