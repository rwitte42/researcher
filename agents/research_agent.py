# This is the research agent that will search for articles and summarize them

from openai import OpenAI
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from config.config import DAYS_BACK, MAX_ARTICLES, OUTPUT_DIR
import requests
from utils.swarm import swarm  # Import the Swarm orchestrator

class ResearchAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Verify API keys exist
        if not os.getenv('OPENAI_API_KEY'):
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        if not os.getenv('BING_API_KEY'):
            raise ValueError("BING_API_KEY not found in environment variables")
            
        self.openai_client = OpenAI()
        self.bing_endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
        self.bing_headers = {"Ocp-Apim-Subscription-Key": os.getenv('BING_API_KEY')}
        
        # Subscribe to research_request event
        swarm.subscribe('research_request', self.handle_research_request)

    def handle_research_request(self, data):
        query = data.get('query')
        days_back = data.get('days_back')
        results = self.perform_research(query, days_back)
        # Publish research_completed event
        swarm.publish('research_completed', {'results': results})

    def format_date_range(self):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=DAYS_BACK)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def search_articles(self, topic):
        # Search for articles using Bing News API
        try:
            params = {
                "q": topic,
                "count": MAX_ARTICLES,
                "freshness": f"Day",  # Can be: Day, Week, Month
                "textFormat": "Raw",
                "safeSearch": "Moderate"
            }
            
            response = requests.get(
                self.bing_endpoint,
                headers=self.bing_headers,
                params=params
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            
            search_results = response.json()
            return search_results.get("value", [])
            
        except Exception as e:
            print(f"Error searching articles: {str(e)}")
            return []

    def summarize_article(self, title, description, url):
        prompt = f"""
        Please provide a 2-3 sentence summary of this article:
        Title: {title}
        Content: {description}
        
        Keep the summary factual and concise.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        
        return response.choices[0].message.content

    def perform_research(self, query, days_back):
        # Perform the actual research
        articles = self.search_articles(query)
        
        if not articles:
            return "No recent articles found for this topic."
        
        # Process each article
        research_results = []
        for article in articles:
            title = article.get('name', 'No title available')
            description = article.get('description', 'No content available')
            url = article.get('url', '#')
            date_published = article.get('datePublished', '')
            
            # Convert date to more readable format
            try:
                date_obj = datetime.strptime(date_published, "%Y-%m-%dT%H:%M:%S.%fZ")
                date_formatted = date_obj.strftime("%B %d, 2023")
            except:
                date_formatted = date_published
            
            # Get AI-generated summary
            summary = self.summarize_article(title, description, url)
            
            # Format in markdown
            article_md = f"""
## {title}
**Published:** {date_formatted}

{summary}

[Read More]({url})
"""
            research_results.append(article_md)
        
        # Combine all results
        final_results = "\n".join(research_results)
        
        return final_results
