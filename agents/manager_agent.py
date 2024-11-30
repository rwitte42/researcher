# This is the manager agent that will handle the interaction with the user

from agents.time_parser_agent import TimeParserAgent
from agents.research_agent import ResearchAgent
from agents.output_agent import OutputAgent  # Import the OutputAgent

class ManagerAgent:
    def __init__(self):
        self.time_parser = TimeParserAgent()
        self.research_agent = ResearchAgent()
        self.output_agent = OutputAgent()  # Initialize the OutputAgent

    def collect_input(self):
        time_input = input("How far back would you like to search? (e.g., '2 weeks', '3 months', '1 quarter') or enter a number of days (1-365): ")
        query_input = input("What research topic would you like to explore? ")

        return time_input, query_input

    def handle_interaction(self):
        time_input, query_input = self.collect_input()
        
        # Get the number of days back
        days_back = self.time_parser.get_days_back(time_input)
        
        # Call the research agent with the query and days back
        results = self.research_agent.perform_research(query_input, days_back)
        
        # Write the results to a Markdown file using OutputAgent
        self.output_agent.write_results_to_md(results)

    def get_valid_days(self):
        parser = TimeParserAgent()
        
        while True:
            try:
                time_input = input("\nHow far back would you like to search? (e.g., '2 weeks', '3 months', '1 quarter')\nOr enter a number of days (1-365): ")
                
                # First try to parse as a direct number
                try:
                    days = int(time_input)
                    if 1 <= days <= 365:
                        return days
                    print("Please enter a number between 1 and 365.")
                    continue
                except ValueError:
                    pass
                
                # If not a number, try to parse as a time period
                days, explanation = parser.get_days_back(time_input)
                print(f"\nInterpreted as {days} days ({explanation})")
                return days  # Directly return the interpreted days
                
            except ValueError as e:
                print(f"\nError: {str(e)}")
                print("Please try again with a different format.")

# Example usage
if __name__ == "__main__":
    manager = ManagerAgent()
    manager.handle_interaction() 