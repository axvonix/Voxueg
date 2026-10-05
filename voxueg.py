#!/usr/bin/env python3
# Voxueg - Tools Termux | Dev: Alzeoxyz
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import modules  # noqa: F401  (mendaftarkan semua fitur)
from core.menu import main

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n  Keluar. - Alzeoxyz")
