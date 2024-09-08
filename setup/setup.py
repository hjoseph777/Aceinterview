# setup.py
import os
import subprocess
import sys
import logging
from datetime import datetime
from setuptools import setup, find_packages
import signal

# Get the user's profile directory
user_profile = os.environ.get("USERPROFILE")

# Define the virtual environment directory
venv_directory = os.path.join(user_profile, ".venvs", "Aceinterview")
# Define the log directory in the user's AppData directory
app_data_directory = os.path.join(os.environ.get("LOCALAPPDATA"), "Aceinterview")
log_directory = os.path.join(app_data_directory, "logs")

# Get the current date
current_date = datetime.now().strftime("%Y%m%d")

# Define the log file name with the current date
log_file_name = os.path.join(log_directory, f"{current_date}_error.log")

# Ensure the log directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Configure logging
logging.basicConfig(
    filename=log_file_name,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

# Optionally, add a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logging.getLogger().addHandler(console_handler)

def create_virtualenv():
    if not os.path.exists(venv_directory):
        try:
            logging.info("Creating virtual environment...")
            print("Creating virtual environment...")
            subprocess.check_call([sys.executable, "-m", "venv", venv_directory])
            logging.info("Virtual environment created.")
            print("Virtual environment created.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Error creating virtual environment: {e}")
            print(f"Error creating virtual environment: {e}")
            sys.exit(1)
    else:
        logging.info("Virtual environment already exists.")
        print("Virtual environment already exists.")

def deactivate_virtualenv():
    if os.name == 'nt':
        deactivate_script = os.path.join(venv_directory, "Scripts", "deactivate.bat")
    else:
        deactivate_script = os.path.join(venv_directory, "bin", "deactivate")
    if os.path.exists(deactivate_script):
        subprocess.call(deactivate_script, shell=True)
        logging.info("Virtual environment deactivated.")
        print("Virtual environment deactivated.")

def activate_virtualenv():
    if os.name == 'nt':
        activate_script = os.path.join(venv_directory, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(venv_directory, "bin", "activate")
    return activate_script

def install_dependencies():
    try:
        logging.info("Installing dependencies...")
        print("Installing dependencies...")
        requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "requirements.txt")
        #requirements_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requirements.txt")
        if not os.path.exists(requirements_path):
            logging.error(f"requirements.txt not found at {requirements_path}")
            print(f"requirements.txt not found at {requirements_path}")
            sys.exit(1)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        logging.info("Dependencies installed.")
        print("Dependencies installed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing dependencies: {e}")
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def signal_handler(sig, frame):
    logging.info("Exiting gracefully...")
    print("Exiting gracefully...")
    sys.exit(0)

# Register the signal handler for SIGINT and SIGTERM
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def run_main():
    try:
        logging.info("Running main.py...")
        print("Running main.py...")
        #subprocess.check_call([sys.executable, "main.py"])
        main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "main.py")
        subprocess.check_call([sys.executable, main_path])
        logging.info("main.py executed successfully.")
        print("main.py executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error running main.py: {e}")
        print(f"Error running main.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        create_virtualenv()
        deactivate_virtualenv()
        activate_script = activate_virtualenv()
        logging.info(f"Run the following command to activate the virtual environment:\n{activate_script}")
        print(f"Run the following command to activate the virtual environment:\n{activate_script}")
        install_dependencies()
        run_main()
        logging.info("Setup complete.")
        print("Setup complete.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
        sys.exit(1)

setup(
    name="aceinterview",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aceinterview=run_aceinterview:main',
        ],
    },
)