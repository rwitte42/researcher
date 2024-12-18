# This is the research agent that will search for articles and summarize them

import logging
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
from config.config import DAYS_BACK, MAX_ARTICLES, OUTPUT_DIR
from utils.swarm import swarm  # Import the Swarm orchestrator

logger = logging.getLogger(__name__)

class ResearchAgent:
    _subscribed = False  # Class variable to track subscription

    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Verify API keys exist
        if not os.getenv('OPENAI_API_KEY'):
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        if not os.getenv('BING_API_KEY'):
            logger.error("BING_API_KEY not found in environment variables")
            raise ValueError("BING_API_KEY not found in environment variables")
            
        self.openai_client = OpenAI()
        self.bing_endpoint = "https://api.bing.microsoft.com/v7.0/news/search"
        self.bing_headers = {"Ocp-Apim-Subscription-Key": os.getenv('BING_API_KEY')}
        
        # Subscribe to research_request event only once
        if not ResearchAgent._subscribed:
            swarm.subscribe('research_request', self.handle_research_request)
            ResearchAgent._subscribed = True
            logger.debug("Subscribed to 'research_request' event.")

    def handle_research_request(self, data):
        logger.info("handle_research_request called with data: %s", data)
        query = data.get('query')
        days_back = data.get('days_back')
        logger.info(f"Received research request for '{query}' over {days_back} days.")
        results = self.perform_research(query, days_back)
        
        # Publish research_completed event
        print(f"Research completed for '{query}' over {days_back} days.")
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
                "freshness": "Day",  # Can be: Day, Week, Month
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
            logger.debug(f"Found {len(search_results.get('value', []))} articles for topic '{topic}'.")
            return search_results.get("value", [])
            
        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
            return []

    def summarize_article(self, title, description, url):
        prompt = f"""
        Please provide a 2-3 sentence summary of this article:
        Title: {title}
        Content: {description}
        
        Keep the summary factual and concise.
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            summary = response.choices[0].message.content.strip()
            logger.debug(f"Summarized article '{title}'.")
            return summary
        except Exception as e:
            logger.error(f"Error summarizing article '{title}': {str(e)}")
            return "Summary not available."

    def perform_research(self, query, days_back):
        # Perform the actual research
        articles = self.search_articles(query)
        
        if not articles:
            logger.info("No recent articles found for this topic.")
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
                date_formatted = date_obj.strftime("%B %d, %Y")
            except ValueError:
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
        
        logger.info(f"Research completed for topic '{query}'.")
        return final_results
