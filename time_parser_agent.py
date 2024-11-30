from openai import OpenAI
from dotenv import load_dotenv
import os
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

    def get_days_back(self, time_input):
        """
        Convert a natural language time input to number of days.
        Returns tuple of (days, explanation) or raises ValueError if invalid.
        Maximum allowed is 365 days.
        """
        prompt = f"""
        Convert this time period to days: "{time_input}"
        Maximum allowed is 365 days.
        
        Common conversions:
        - 1 week = 7 days
        - 1 month = 30 days
        - 1 quarter = 90 days
        - 1 year = 365 days
        
        If the input is unclear or invalid, respond with a question starting with "CLARIFY:".
        If the time period exceeds 365 days, return exactly 365 days.
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
                raise ValueError(result.split("CLARIFY:")[1].strip())
            
            # Parse the JSON response
            parsed = json.loads(result)
            days = min(int(parsed["days"]), 365)  # Ensure we don't exceed 365 days
            
            return days, parsed["explanation"]
            
        except Exception as e:
            raise ValueError(f"Error parsing time input: {str(e)}")

# Add this line at the end of the file
__all__ = ['TimeParserAgent']