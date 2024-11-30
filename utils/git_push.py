import os
import subprocess

def git_push_all():
    # Prompt for a descriptive commit message
    commit_message = input("Enter a descriptive commit message: ")

    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit the changes with the provided message
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push to the main branch
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("All changes have been pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    git_push_all() 