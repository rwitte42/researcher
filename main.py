# This is the main script that will run the research agent

from agents.time_parser_agent import TimeParserAgent
from agents.research_agent import ResearchAgent
from config.config import OUTPUT_DIR, OPENAI_MODEL
import openai

def get_valid_days():
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
            
            confirm = input("Is this correct? (y/n): ").lower().strip()
            if confirm.startswith('y'):
                return days
            
        except ValueError as e:
            print(f"\nError: {str(e)}")
            print("Please try again with a different format.")

def main():
    try:
        # Initialize the research agent
        agent = ResearchAgent()
        
        # Get topic from user first
        topic = input("Enter the research topic: ")
        
        # Then get time period from user
        days_back = get_valid_days()
        
        print(f"\nResearching '{topic}' for the past {days_back} days... This may take a few moments.")
        
        # Perform research
        results = agent.research_topic(topic, days_back)
        
        print("\nResearch completed! Results have been saved to the research_results directory.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 