import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from src.rsvp_bot import run_bot

if __name__ == "__main__":
    run_bot()
