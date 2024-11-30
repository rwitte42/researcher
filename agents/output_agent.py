import os
from config.config import OUTPUT_DIR

class OutputAgent:
    def __init__(self):
        # Ensure the output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def write_results_to_md(self, results):
        # Define the output file path
        output_file = os.path.join(OUTPUT_DIR, "research_results.md")
        
        # Write results to the Markdown file
        with open(output_file, 'w') as f:
            f.write("# Research Results\n\n")
            f.write(results)
        
        print(f"Results written to {output_file}") 