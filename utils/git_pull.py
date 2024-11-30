import subprocess

def git_pull():
    # Prompt for the branch name
    branch_name = input("Enter the branch name to pull from: ")
    
    try:
        # Pull updates from the specified branch
        subprocess.run(["git", "pull", "origin", branch_name], check=True)
        print(f"Successfully pulled updates from the '{branch_name}' branch.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while pulling updates: {e}")

if __name__ == "__main__":
    git_pull() 