# This is the configuration file for the project

from datetime import datetime, timedelta
import os

# Configuration settings
DAYS_BACK = 7  # Easily modifiable time period
MAX_ARTICLES = 10
OUTPUT_DIR = os.path.expanduser("~/Desktop/research_results")  # This is the output directory

# Update OpenAI model configuration
OPENAI_MODEL = 'gpt-4o1-mini'
