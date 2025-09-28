#!/usr/bin/env python3
"""
RGB LED Button Service for Tinkerforge
Manages 3 RGB LED buttons that can execute programs when pressed.
"""

import time
import subprocess
import threading
import signal
import sys
from typing import Dict, Optional, Tuple
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton


class ButtonService:
    def __init__(self):
        # Hardcoded button UIDs - replace with your actual button UIDs
        self.button_uids = [
            "2dxQ",  # Replace with actual UID of button 1
            "2dyi",  # Replace with actual UID of button 2
            "2dy4" # Replace with actual UID of button 3
        ]
        
        # Hardcoded programs to execute - replace with your actual programs
        self.programs = [
            "../depthai_hand_tracker/demo.py -e",  # Program for button 1
            "hello.mp3",    # MP3 file for button 2
            "mehring.mp3"   # MP3 file for button 3
        ]
        
        # Colors (R, G, B) - each value 0-255
        self.color_blue = (0, 0, 255)
        self.color_cyan = (0, 255, 255)
        
        # State management
        self.running_processes: Dict[int, subprocess.Popen] = {}
        self.button_objects: Dict[int, BrickletRGBLEDButton] = {}
        self.ipcon = IPConnection()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        print("\nShutting down button service...")
        self.cleanup()
        sys.exit(0)
    
    def connect_to_buttons(self):
        """Connect to the Tinkerforge daemon and initialize buttons."""
        try:
            # Connect to brickd (Tinkerforge daemon)
            self.ipcon.connect("localhost", 4223)
            print("Connected to Tinkerforge daemon")
            
            # Initialize each button
            for i, uid in enumerate(self.button_uids):
                try:
                    button = BrickletRGBLEDButton(uid, self.ipcon)
                    self.button_objects[i] = button
                    
                    # Set initial color to blue
                    button.set_color(*self.color_blue)
                    print(f"Button {i+1} (UID: {uid}) initialized and set to blue")
                    
                    # Register button state callback
                    button.register_callback(
                        button.CALLBACK_BUTTON_STATE_CHANGED,
                        lambda state, button_id=i: self.button_callback(button_id, state)
                    )
                    
                except Exception as e:
                    print(f"Error initializing button {i+1} (UID: {uid}): {e}")
                    # Remove from button_objects if initialization failed
                    if i in self.button_objects:
                        del self.button_objects[i]
            
            if not self.button_objects:
                raise Exception("No buttons could be initialized")
                
        except Exception as e:
            print(f"Error connecting to buttons: {e}")
            raise
    
    def button_callback(self, button_id: int, state: int):
        """Handle button press/release events."""
        print(f"Button {button_id+1} state changed: {state}")
        
        # Only handle button press (state = 1), ignore release (state = 0)
        if state == 1:
            self.handle_button_press(button_id)
    
    def handle_button_press(self, button_id: int):
        """Handle button press - start or stop program."""
        if button_id in self.running_processes:
            # Program is running, stop it
            self.stop_program(button_id)
        else:
            # No program running, start it
            self.start_program(button_id)
    
    def start_program(self, button_id: int):
        """Start the program associated with the button."""
        if button_id >= len(self.programs):
            print(f"No program defined for button {button_id+1}")
            return
        
        program = self.programs[button_id]
        print(f"Starting program: {program}")
        
        try:
            # Determine command based on file extension
            if program.endswith('.mp3'):
                # Use mpg123 to play MP3 files
                cmd = ["mpg123", program]
            elif program.endswith('.py'):
                # Use python3 for Python scripts
                cmd = ["python3", program]
            else:
                # Default to python3 for unknown extensions
                cmd = ["python3", program]
            
            # Start the program
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd="."  # Run in current directory
            )
            
            # Store the process
            self.running_processes[button_id] = process
            
            # Change button color to cyan
            if button_id in self.button_objects:
                self.button_objects[button_id].set_color(*self.color_cyan)
                print(f"Button {button_id+1} changed to cyan")
            
            # Start monitoring thread for this process
            monitor_thread = threading.Thread(
                target=self.monitor_process,
                args=(button_id, process),
                daemon=True
            )
            monitor_thread.start()
            
        except Exception as e:
            print(f"Error starting program {program}: {e}")
    
    def stop_program(self, button_id: int):
        """Stop the program associated with the button."""
        if button_id not in self.running_processes:
            return
        
        process = self.running_processes[button_id]
        print(f"Stopping program for button {button_id+1}")
        
        try:
            # Terminate the process
            process.terminate()
            
            # Wait for graceful termination
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if it doesn't terminate gracefully
                process.kill()
                process.wait()
            
            # Remove from running processes
            del self.running_processes[button_id]
            
            # Change button color back to blue
            if button_id in self.button_objects:
                self.button_objects[button_id].set_color(*self.color_blue)
                print(f"Button {button_id+1} changed back to blue")
                
        except Exception as e:
            print(f"Error stopping program for button {button_id+1}: {e}")
    
    def monitor_process(self, button_id: int, process: subprocess.Popen):
        """Monitor a running process and handle its completion."""
        try:
            # Wait for the process to complete
            return_code = process.wait()
            print(f"Program for button {button_id+1} finished with return code: {return_code}")
            
            # Remove from running processes if still there
            if button_id in self.running_processes:
                del self.running_processes[button_id]
            
            # Change button color back to blue
            if button_id in self.button_objects:
                self.button_objects[button_id].set_color(*self.color_blue)
                print(f"Button {button_id+1} changed back to blue")
                
        except Exception as e:
            print(f"Error monitoring process for button {button_id+1}: {e}")
    
    def cleanup(self):
        """Clean up resources and stop all running programs."""
        print("Cleaning up...")
        
        # Stop all running programs
        for button_id in list(self.running_processes.keys()):
            self.stop_program(button_id)
        
        # Disconnect from IP connection
        try:
            self.ipcon.disconnect()
            print("Disconnected from Tinkerforge daemon")
        except:
            pass
    
    def run(self):
        """Main run loop."""
        try:
            print("Starting RGB LED Button Service...")
            print("Press Ctrl+C to stop")
            
            # Connect to buttons
            self.connect_to_buttons()
            
            print(f"Service running with {len(self.button_objects)} buttons")
            print("Button states:")
            for i in range(len(self.button_uids)):
                if i in self.button_objects:
                    print(f"  Button {i+1}: Ready (blue)")
                else:
                    print(f"  Button {i+1}: Not connected")
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nReceived keyboard interrupt")
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            self.cleanup()


def main():
    """Main entry point."""
    service = ButtonService()
    service.run()


if __name__ == "__main__":
    main()
