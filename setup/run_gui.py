# run_gui.py
import subprocess
import sys
import os
import signal

def graceful_exit(signum, frame):
    print("Gracefully exiting...")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, graceful_exit)
    signal.signal(signal.SIGTERM, graceful_exit)
    
    try:
        print("Running gui.py...")
        gui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gui.py")
        subprocess.check_call([sys.executable, gui_path])
        print("gui.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running gui.py: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()