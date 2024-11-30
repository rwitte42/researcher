from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
import json

class TimeParserAgent:
    def __init__(self):
        # Load environment variables from .env
        load_dotenv()
        
        # Get API key from environment
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
            
        # Initialize OpenAI client with API key
        self.client = OpenAI(api_key=self.api_key)

    def parse_time_to_days(self, time_input):
        if time_input.lower() in ['q', 'quit', 'exit']:
            print("\nGoodbye!")
            sys.exit(0)
            
        prompt = f"""
        Convert this time period to days: "{time_input}"
        
        Common conversions:
        - 1 week = 7 days
        - 1 month = 30 days
        - 1 quarter = 90 days
        - 1 year = 365 days
        
        If the input is unclear or needs clarification, respond with a question starting with "CLARIFY:".
        Otherwise, respond ONLY with a JSON object in this exact format:
        {{
            "days": number_of_days,
            "explanation": "brief explanation of how this was calculated"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful time parsing assistant. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            result = response.choices[0].message.content
            
            # Check if clarification is needed
            if "CLARIFY:" in result:
                return {"needs_clarification": True, "question": result.split("CLARIFY:")[1].strip()}
            
            # Parse the JSON response
            parsed = json.loads(result)
            return {
                "needs_clarification": False,
                "days": int(parsed["days"]),
                "explanation": parsed["explanation"]
            }
            
        except Exception as e:
            raise ValueError(f"Error parsing time input: {str(e)}")

def main():
    parser = TimeParserAgent()
    
    print("Time Parser - Convert time periods to days")
    print("Enter 'q' or 'quit' to exit")
    
    while True:
        try:
            time_input = input("\nEnter a time period (e.g., '2 weeks', '3 months', '1 quarter'): ")
            
            result = parser.parse_time_to_days(time_input)
            
            if result.get("needs_clarification"):
                print(f"\nClarification needed: {result['question']}")
                continue
                
            print(f"\nCalculated days: {result['days']}")
            print(f"Explanation: {result['explanation']}")
            
            confirm = input("\nWould you like to try another? (y/n): ").lower().strip()
            if confirm != 'y' and confirm != 'yes':
                print("\nGoodbye!")
                break
                
        except ValueError as e:
            print(f"Error: {str(e)}")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break

if __name__ == "__main__":
    main()