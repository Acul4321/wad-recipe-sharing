import subprocess
import sys
import os

def run_command(command, error_message):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"Error: {error_message}")
        sys.exit(1)

def main():
    print("Setting up Recipe Sharing project...")

    # Install dependencies
    print("Installing dependencies from requirements.txt...")
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                "Failed to install dependencies")

    # Make migrations
    print("Making migrations...")
    run_command([sys.executable, "manage.py", "makemigrations"],
                "Failed to make migrations")

    # Apply migrations
    print("Applying migrations...")
    run_command([sys.executable, "manage.py", "migrate"],
                "Failed to apply migrations")

    # Populate database
    print("Populating database...")
    run_command([sys.executable, "populate_world_recipe.py"],
                "Failed to populate database")

    print("Setup complete!")

if __name__ == "__main__":
    main()
