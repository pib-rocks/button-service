#!/usr/bin/env python3
"""
Example program 3 - Interactive program
This program runs indefinitely until stopped, showing periodic status updates.
"""

import time
import signal
import sys

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    print("\nProgram 3: Received shutdown signal, cleaning up...")
    sys.exit(0)

def main():
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Program 3: Starting interactive program...")
    print("This program will run until stopped by the button service.")
    
    counter = 0
    while True:
        counter += 1
        print(f"Program 3: Status update #{counter}")
        time.sleep(5)

if __name__ == "__main__":
    main()
