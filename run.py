import sys
import os

# Add the src directory to the system path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Run the main application
from src.GUI.main import main

if __name__ == "__main__":
    main()