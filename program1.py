#!/usr/bin/env python3
"""
Example program 1 - Simple counter
This program counts from 1 to 10 with a 1-second delay between each count.
"""

import time

def main():
    print("Program 1: Starting counter...")
    
    for i in range(1, 11):
        print(f"Count: {i}")
        time.sleep(1)
    
    print("Program 1: Counter finished!")

if __name__ == "__main__":
    main()
