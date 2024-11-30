# This is the output agent that handles writing results to a Markdown file

import logging
import os
from datetime import datetime
from config.config import OUTPUT_DIR
from utils.swarm import swarm  # Import the Swarm orchestrator

logger = logging.getLogger(__name__)

class OutputAgent:
    def __init__(self):
        # Subscribe to results_ready event
        swarm.subscribe('results_ready', self.handle_results_ready)

    def handle_results_ready(self, data):
        #Define results and output path variables
        results = data.get('results')
        output_path = self.write_results_to_md(results)
        
        # Notify the ManagerAgent with the output path
        swarm.publish('results_written', {'output_path': output_path})

    def write_results_to_md(self, results):
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
                logger.debug(f"Created output directory at '{OUTPUT_DIR}'.")
                
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
            return filename  # Return the filename for confirmation
        except Exception as e:
            logger.error(f"Error writing results to file: {str(e)}")
            return None  # Return None if there was an error