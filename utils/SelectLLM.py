# This is the utility script to select the LLM

import sys
import os

# Add the parent directory and the utils directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'utils'))

from config.llm_list import LLM_OPTIONS
from config.config import OPENAI_MODEL

def display_llm_options():
    print("Available LLMs:")
    for index, llm in enumerate(LLM_OPTIONS, start=1):
        print(f"{index}. {llm}")
    print("Q. Quit")

def update_config(selected_llm):
    # Update the config.py file with the selected LLM
    config_file_path = 'config/config.py'
    
    with open(config_file_path, 'r') as file:
        lines = file.readlines()

    with open(config_file_path, 'w') as file:
        for line in lines:
            if line.startswith("OPENAI_MODEL"):
                file.write(f"OPENAI_MODEL = '{selected_llm}'\n")
            else:
                file.write(line)

def main():
    while True:
        display_llm_options()
        choice = input("Select an LLM by number or press Q to quit: ").strip().lower()

        if choice == 'q':
            print("Exiting...")
            break

        if choice.isdigit() and 1 <= int(choice) <= len(LLM_OPTIONS):
            selected_llm = LLM_OPTIONS[int(choice) - 1]
            update_config(selected_llm)
            print(f"Updated LLM to: {selected_llm}")
            break  # Exit after a valid selection
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 