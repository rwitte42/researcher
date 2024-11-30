# This is the manager agent that will handle the interaction with the user

import logging
from agents.time_parser_agent import TimeParserAgent
from agents.research_agent import ResearchAgent
from agents.output_agent import OutputAgent  # Import the OutputAgent
from utils.swarm import swarm  # Import the Swarm orchestrator

logger = logging.getLogger(__name__)

class ManagerAgent:
    def __init__(self):
        self.time_parser = TimeParserAgent()
        self.research_agent = ResearchAgent()
        self.output_agent = OutputAgent()  # Initialize the OutputAgent
        
        # Subscribe to research_completed event
        swarm.subscribe('research_completed', self.handle_research_completed)

    def collect_input(self):
        time_input = self.get_valid_days()  # Get valid days directly
        query_input = input("What research topic would you like to explore? ")

        return time_input, query_input

    def handle_interaction(self):
        time_input, query_input = self.collect_input()
        
        # Publish a research_request event
        logger.info(f"Publishing research_request for topic '{query_input}' over {time_input} days.")
        swarm.publish('research_request', {'query': query_input, 'days_back': time_input})

    def get_valid_days(self):
        while True:
            try:
                time_input = input("\nHow far back would you like to search? (e.g., '2 weeks', '3 months', '1 quarter')\nOr enter a number of days (1-365): ")
                
                # First try to parse as a direct number
                try:
                    days = int(time_input)
                    if 1 <= days <= 365:
                        return days
                    logger.info("Please enter a number between 1 and 365.")
                    continue
                except ValueError:
                    pass
                
                # If not a number, try to parse as a time period
                days, explanation = self.time_parser.get_days_back(time_input)
                logger.info(f"Interpreted as {days} days ({explanation})")
                return days  # Directly return the interpreted days
                
            except ValueError as e:
                logger.warning(f"Error: {str(e)}")
                logger.info("Please try again with a different format.")

    def handle_research_completed(self, data):
        results = data.get('results')
        logger.info("Research completed. Publishing results_ready event.")
        # Publish a results_ready event
        swarm.publish('results_ready', {'results': results})

# Example usage
if __name__ == "__main__":
    manager = ManagerAgent()
    manager.handle_interaction() 