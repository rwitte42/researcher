# This is the main script that will run the research agent

from agents.manager_agent import ManagerAgent  # Import the ManagerAgent
from agents.research_agent import ResearchAgent
from agents.output_agent import OutputAgent

def main():
    try:
        # Initialize all agents
        manager = ManagerAgent()
        research_agent = ResearchAgent()
        output_agent = OutputAgent()
        
        # Handle interaction with the user
        manager.handle_interaction()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 