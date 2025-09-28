#!/usr/bin/env python3
"""
Example program 2 - Long running task
This program simulates a long-running task that takes 30 seconds.
"""

import time

def main():
    print("Program 2: Starting long task...")
    
    for i in range(30):
        print(f"Task progress: {i+1}/30 seconds")
        time.sleep(1)
    
    print("Program 2: Long task completed!")

if __name__ == "__main__":
    main()
