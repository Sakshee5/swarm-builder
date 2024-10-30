from configs.agents import *
from swarm.repl import run_demo_loop

context_variables = {'user_name': 'sakshee', 'swarm_name': 'AI Health Coach', 'swarm_structure': '[[manager], [manager, health_assessment], [health_assessment, manager], [manager, nutrition_coach], [nutrition_coach, manager], [manager, fitness_coach], [fitness_coach, manager], [manager, stress_manager], [stress_manager, manager], [manager, motivation_specialist], [motivation_specialist, manager]]'}

if __name__ == "__main__":
    run_demo_loop(manager, context_variables=context_variables, stream=True, debug=True)