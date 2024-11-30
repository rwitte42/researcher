import os
from agents.time_parser_agent import TimeParserAgent
from agents.research_agent import ResearchAgent
from config import OUTPUT_DIR  # Import the OUTPUT_DIR from config

class ManagerAgent:
    def __init__(self):
        self.time_parser = TimeParserAgent()
        self.research_agent = ResearchAgent()

    def collect_input(self):
        time_input = input("How far back would you like to search? (e.g., '2 weeks', '3 months', '1 quarter') or enter a number of days (1-365): ")
        query_input = input("What research topic would you like to explore? ")

        return time_input, query_input

    def write_results_to_md(self, results):
        # Ensure the output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # Define the output file path
        output_file = os.path.join(OUTPUT_DIR, "research_results.md")
        
        # Write results to the Markdown file
        with open(output_file, 'w') as f:
            f.write("# Research Results\n\n")
            f.write(results)
        
        print(f"Results written to {output_file}")

    def handle_interaction(self):
        time_input, query_input = self.collect_input()
        
        # Get the number of days back
        days_back = self.time_parser.get_days_back(time_input)
        
        # Call the research agent with the query and days back
        results = self.research_agent.perform_research(query_input, days_back)
        
        # Write the results to a Markdown file
        self.write_results_to_md(results)  # Use the output directory from config

# Example usage
if __name__ == "__main__":
    manager = ManagerAgent()
    manager.handle_interaction() 