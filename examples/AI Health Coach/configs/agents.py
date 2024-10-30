# Agents configuration file



from configs.tools import *
from swarm import Agent

def manager_instructions():
    return """Acts as the central point of interaction for the user. Routes tasks to specific agents based on user needs. Receives reports from specialized agents."""



manager = Agent(
    name="manager",
    instructions=manager_instructions(),
    functions=[communication_tool],
)




def health_assessment_instructions():
    return """Conducts initial assessments and identifies health risks. Communicates with the manager to report findings."""



health_assessment = Agent(
    name="health_assessment",
    instructions=health_assessment_instructions(),
    functions=[health_data_analysis_api],
)




def nutrition_coach_instructions():
    return """Offers personalized dietary advice, utilizing data from the health assessment agent. Communicates with the manager."""



nutrition_coach = Agent(
    name="nutrition_coach",
    instructions=nutrition_coach_instructions(),
    functions=[nutritional_database, diet_tracker_api],
)




def fitness_coach_instructions():
    return """Creates personalized fitness plans. Collaborates with the manager to deliver tailored activity recommendations."""



fitness_coach = Agent(
    name="fitness_coach",
    instructions=fitness_coach_instructions(),
    functions=[fitness_recommendation_engine, activity_tracker_api],
)




def stress_manager_instructions():
    return """Offers stress management strategies based on assessment. Reports and advises through the manager."""



stress_manager = Agent(
    name="stress_manager",
    instructions=stress_manager_instructions(),
    functions=[stress_assessment_tool, meditation_library],
)




def motivation_specialist_instructions():
    return """Uses behavioral science to promote habit change, interfacing with the manager to enhance user motivation."""



motivation_specialist = Agent(
    name="motivation_specialist",
    instructions=motivation_specialist_instructions(),
    functions=[behavioral_tracking_tool, motivational_content_library],
)
