import subprocess

def git_pull():
    try:
        # Pull updates from the remote repository
        subprocess.run(["git", "pull", "origin", "main"], check=True)
        print("Successfully pulled updates from the remote repository.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while pulling updates: {e}")

if __name__ == "__main__":
    git_pull() 