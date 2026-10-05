import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modules  # noqa: F401
from core.menu import main

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Keluar. - Alzeoxyz")
