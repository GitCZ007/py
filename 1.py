import sys
import subprocess

def get_environment_info():
    # 1. Get the current Python Version
    print("=" * 40)
    print(f"Python Version: {sys.version}")
    print("=" * 40)
    
    # 2. Run 'pip list' and capture the output safely
    print("\nInstalled Libraries (pip list):")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving pip list: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")

if __name__ == "__main__":
    get_environment_info()
