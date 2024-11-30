import subprocess

def git_push():
    # Prompt for the branch name
    branch_name = input("Enter the branch name to push: ")
    
    # Prompt for the commit message
    commit_message = input("Enter the commit message: ")
    
    try:
        # Stage all changes
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push updates to the specified branch
        subprocess.run(["git", "push", "origin", branch_name], check=True)
        print(f"Successfully pushed updates to the '{branch_name}' branch.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    git_push() 