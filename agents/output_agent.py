# This is the output agent that handles writing results to a Markdown file

import os
from datetime import datetime
from config.config import OUTPUT_DIR
from utils.swarm import swarm  # Import the Swarm orchestrator

class OutputAgent:
    def __init__(self):
        # Subscribe to results_ready event
        swarm.subscribe('results_ready', self.handle_results_ready)

    def handle_results_ready(self, data):
        results = data.get('results')
        self.write_results_to_md(results)

    def write_results_to_md(self, results):
        # Create output directory if it doesn't exist
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            
        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{OUTPUT_DIR}/research_results_{timestamp}.md"
        
        # Add header to the results
        header = f"""# Research Results
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(header + results)
        
        print(f"Research results saved to {filename}") 