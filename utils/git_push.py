import os
import subprocess

def git_push_all(commit_message="Push all changes"):
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push to the main branch
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("All changes have been pushed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # You can customize the commit message here
    git_push_all("Push all changes") 