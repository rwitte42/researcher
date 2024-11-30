# This is the manager agent that will handle the interaction with the user

import logging
import random  # Import random for generating varied greetings
from agents.time_parser_agent import TimeParserAgent
from agents.research_agent import ResearchAgent
from agents.output_agent import OutputAgent  # Import the OutputAgent
from utils.swarm import swarm  # Import the Swarm orchestrator

logger = logging.getLogger(__name__)

class ManagerAgent:
    def __init__(self):
        self.time_parser = TimeParserAgent() # Initialize the TimeParserAgent
        self.research_agent = ResearchAgent() # Initialize the ResearchAgent
        self.output_agent = OutputAgent()  # Initialize the OutputAgent
        
        # Log the swarm instance ID
        logger.debug(f"ManagerAgent is using swarm instance ID: {id(swarm)}")

        # Subscribe to research_completed event
        swarm.subscribe('research_completed', self.handle_research_completed)

    def collect_input(self):
        # Ask for topic
        query_input = input("What research topic would you like to explore? ")

        # Ask for the time frame
        time_input = self.get_valid_days()  
        
        # Display the topic and time frame back to the user
        print(f"\nSearching for articles on '{query_input}' from the last {time_input} days.\n")  # Confirm search parameters

        return time_input, query_input

    def handle_interaction(self):
        # Display a friendly greeting
        print(f"Hi there! I'm here to assist you with your research. Just let me know the topic and the time frame, and I'll provide you with the results in a Markdown file.")

        # Collect the input from the user
        time_input, query_input = self.collect_input()
        
        # Publish a research_request event
        print("Awaiting results...") # Simple message back to the user indicating that results are being awaited
        swarm.publish('research_request', {'query': query_input, 'days_back': time_input}) # Request the research from the research agent

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
        # Get the results from the research agent
        results = data.get('results')
        
        # Publish a results_ready event
        swarm.publish('results_ready', {'results': results})
        print("Results ready.")

        # Print a simple confirmation message
        print("Output file written.")

# Example usage
if __name__ == "__main__":
    manager = ManagerAgent()
    manager.handle_interaction()