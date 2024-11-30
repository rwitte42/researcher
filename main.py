# This is the main script that will run the research agent

from utils.logging_config import setup_logging
from agents.manager_agent import ManagerAgent  # Import the ManagerAgent
from agents.research_agent import ResearchAgent
from agents.output_agent import OutputAgent

import logging

def main():
    # Initialize logging
    setup_logging()
    
    try:
        # Initialize all agents
        manager = ManagerAgent()
        research_agent = ResearchAgent()
        output_agent = OutputAgent()
        
        # Handle interaction with the user
        manager.handle_interaction()
        
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 