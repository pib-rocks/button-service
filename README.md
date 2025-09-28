# RGB LED Button Service

A Python service for managing 3 Tinkerforge RGB LED buttons on a Raspberry Pi 5 with Bookworm OS.

## Features

- Manages 3 RGB LED buttons with hardcoded UIDs
- Buttons start in blue color
- Pressing a button executes a predefined program and changes color to cyan
- Pressing a button while a program is running stops that program
- When a program finishes naturally, the button returns to blue
- Graceful shutdown handling

## Setup

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```

2. Install audio player for MP3 support:
   ```bash
   sudo apt install mpg123
   ```

3. Install and start the Tinkerforge daemon (brickd):
   ```bash
   sudo apt update
   sudo apt install brickd
   sudo systemctl start brickd
   sudo systemctl enable brickd
   ```

4. Configure your button UIDs in `button_service.py`:
   - Replace the hardcoded UIDs in the `button_uids` list with your actual button UIDs
   - Update the `programs` list with the programs you want to execute

5. Make sure your programs are executable:
   ```bash
   chmod +x program1.py program2.py program3.py
   ```

## Usage

Run the service:
```bash
python3 button_service.py
```

The service will:
- Connect to the Tinkerforge daemon
- Initialize all 3 buttons and set them to blue
- Listen for button presses
- Execute programs when buttons are pressed
- Handle program termination and button color changes

## Configuration

### Button UIDs
Edit the `button_uids` list in `button_service.py`:
```python
self.button_uids = [
    "ABC",  # Replace with actual UID of button 1
    "DEF",  # Replace with actual UID of button 2
    "GHI"   # Replace with actual UID of button 3
]
```

### Programs
Edit the `programs` list in `button_service.py`:
```python
self.programs = [
    "program1.py",  # Program for button 1
    "hello.mp3",    # MP3 file for button 2
    "program3.py"   # Program for button 3
]
```

The service supports different file types:
- **Python scripts** (`.py`): Executed with `python3`
- **MP3 files** (`.mp3`): Played with `mpg123`
- **Other files**: Default to `python3` execution

### Colors
You can modify the button colors by changing the color values:
```python
self.color_blue = (0, 0, 255)    # RGB values 0-255
self.color_cyan = (0, 255, 255)  # RGB values 0-255
```

## Example Programs

The repository includes three example programs:

- `program1.py`: Simple counter (10 seconds)
- `program2.py`: Long running task (30 seconds)
- `program3.py`: Interactive program (runs until stopped)

## Stopping the Service

Press `Ctrl+C` to stop the service gracefully. All running programs will be terminated and the service will disconnect from the Tinkerforge daemon.

## Troubleshooting

1. **Buttons not connecting**: Make sure brickd is running and the UIDs are correct
2. **Programs not executing**: Check that the program files exist and are executable
3. **Permission errors**: Make sure the service has permission to execute the programs

## Hardware Requirements

- Raspberry Pi 5 with Bookworm OS
- 3x Tinkerforge RGB LED Button Bricklets
- Tinkerforge Master Brick or similar for connection
- Proper wiring and power supply
