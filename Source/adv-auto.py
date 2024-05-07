"""
Advanced Programmable Autoclicker

This script processes data from "click history" files to perform the functions of an advanced autoclicker.

Features:
- Mouse clicks and movements based on coordinates and wait times.
- Key presses based on specified keys and hold times.
- Text writing with specified intervals between letters and wait times.
- Random wait times between specified ranges.
- Ability to click multiple keys at once, such as "win + print screen".
- Support for comments (`#`) and blank lines in click history files.
- `FWRITE` command reads and writes data from a file based on the iteration number.
- Press 'Q' to quit and 'P' to pause or resume.

Usage:
- Run the script without arguments to display instructions and create a click history file.
- Run the script with two arguments: `<click history filename> <number of iterations>` to specify the file and number of iterations.

To terminate the program at any time, press the 'Q' key.
To pause or resume the program, press the 'P' key.

Author: Max Milazzo
"""

import sys
import os
import threading
import pyautogui
import keyboard
from random import random
from time import sleep
from datetime import datetime

# Global flags for pause and stop
pause_flag = threading.Event()
stop_flag = threading.Event()


def run_cycle(directions, total_iter_num):
    """
    Runs a single click cycle based on the provided directions and iteration number.
    """
    
    try:
        for direction in directions:
            command = direction[0].upper()
            
            if command in ["CLICK", "MOUSE"]:
                execute_click_command(direction)
                
            elif command == "PRESS":
                execute_press_command(direction, total_iter_num)
                
            elif command == "WRITE":
                execute_write_command(direction)
                
            elif command == "FWRITE":
                execute_fwrite_command(direction, total_iter_num)
                
            elif command == "SCREENSHOT":
                execute_screenshot_command(direction)
                
            else:
                raise ValueError(f"Unsupported command '{command}' found in directions.")
            
            # Check pause flag
            while pause_flag.is_set():
                sleep(0.1)
            
            # Check stop flag at the end of each iteration
            if stop_flag.is_set():
                print("Stopping the program...")
                return
            
    except Exception as e:
        print(f"Error: {e}\nProgram will terminate in 10 seconds.")
        sleep(10)
        os._exit(1)


def execute_click_command(direction):
    """
    Executes the CLICK command.
    """
    
    x_pos = pyautogui.position()[0] if not direction[1].isnumeric() else int(direction[1])
    y_pos = pyautogui.position()[1] if not direction[2].isnumeric() else int(direction[2])

    # Get wait time and execute the click
    wait_time = get_sleep_time(direction[3])
    pyautogui.click(x=x_pos, y=y_pos)
    sleep(wait_time)


def execute_press_command(direction, total_iter_num):
    """
    Executes the PRESS command.
    """
    
    key = direction[1]
    
    # Perform the key press
    pyautogui.keyDown(key)
    
    # Calculate hold time and wait time
    hold_time = get_sleep_time(direction[2])
    sleep(hold_time)
    
    pyautogui.keyUp(key)

    # Wait time after key press
    wait_time = get_sleep_time(direction[3])
    sleep(wait_time)


def execute_write_command(direction):
    """
    Executes the WRITE command.
    """
    
    # The text to be written
    text = direction[1]

    # Calculate the interval between keystrokes (supporting random ranges)
    interval = get_sleep_time(direction[2])

    # Calculate wait time after writing (supporting random ranges)
    wait_time = get_sleep_time(direction[3])

    # Write the text with the specified interval between keystrokes
    pyautogui.write(text, interval=interval)

    # Pause for the specified wait time
    sleep(wait_time)


def execute_fwrite_command(direction, total_iter_num):
    """
    Executes the FWRITE command: Writes data from a specified file.
    """
    
    filename = direction[1]
    
    # Calculate the interval between keystrokes (supporting random ranges)
    interval = get_sleep_time(direction[2])

    # Calculate wait time after writing (supporting random ranges)
    wait_time = get_sleep_time(direction[3])

    # Read data from the specified file
    with open(filename, "r") as f:
        lines = f.readlines()

    # Get the line for the current iteration
    if total_iter_num < len(lines):
        line_to_write = lines[total_iter_num].strip()
        # Write the line from the file with the specified interval between keystrokes
        pyautogui.write(line_to_write, interval=interval)
    
    # Wait after writing the line
    sleep(wait_time)
    
    
def execute_screenshot_command(direction):
    """
    Executes the SCREENSHOT command: Takes a screenshot and saves it to the specified directory with a filename based on the current timestamp.
    """
    
    # Define the timestamp format
    timestamp_format = "%Y%m%d_%H%M%S"

    # Generate a timestamp string for the filename
    timestamp = datetime.now().strftime(timestamp_format)

    # The specified directory from the command (first argument)
    directory = direction[1]

    # Create the file path by joining the directory and the filename with the timestamp
    file_path = os.path.join(directory, f"screenshot_{timestamp}.png")

    # Take the screenshot and save it to the file path
    pyautogui.screenshot(file_path)

    print(f"Screenshot saved to: {file_path}")


def get_sleep_time(time_str):
    """
    Parses the sleep time, supporting random ranges if specified.
    """
    
    try:
        # Convert time_str to lowercase to handle both 'R' and 'r' prefixes
        time_str = time_str.lower()
        
        if time_str.startswith("r"):
            # Remove the prefix 'r' and check if a range is specified
            time_str = time_str[1:]
            
            # Check if a range (e.g., '0.1-0.2') is specified
            if "-" in time_str:
                # Split the range and calculate the random wait time
                min_time, max_time = map(float, time_str.split("-"))
                return random() * (max_time - min_time) + min_time
            else:
                # Calculate random wait time up to the specified limit
                max_time = float(time_str)
                return random() * max_time
        else:
            # Return the sleep time as a float
            return float(time_str)
    except Exception as e:
        print(f"Error parsing sleep time: {e}\nProgram will terminate in 10 seconds.")
        sleep(10)
        os._exit(1)


def follow_clicks(filename, iterations):
    """
    Initiates click cycle loop using the provided file and number of iterations.
    """
    
    # Read and parse the click history file
    with open(filename, "r") as f:
        lines = f.readlines()

    # Parse directions and ignore blank lines and comments
    directions = []
    for line in lines:
        # Remove comments and whitespace
        clean_line = line.split("#")[0].strip()
        if clean_line:  # Skip blank lines
            directions.append(clean_line.split())

    print("\nOPERATION:")
    print(directions)

    # Prompt the user to begin the autoclicker sequence
    input('\nPress ENTER to start program initiation. Press "Q" to quit and "P" to pause/play.\n')
    
    for x in reversed(range(10)):
        print(f"Starting in {x} seconds.")
        sleep(1)

    # Set up keyboard listeners for 'P' and 'Q' keys
    keyboard.on_press_key("q", stop_program)
    keyboard.on_press_key("p", toggle_pause)

    # Begin the autoclicker sequence
    total_iter_num = 0

    if iterations is not None:
        # Finite iteration loop
        for _ in range(iterations):
            while True:
                # Check stop flag
                if stop_flag.is_set():
                    print("Stopping the program...")
                    return
                
                # Check pause flag
                while pause_flag.is_set():
                    sleep(0.1)
                
                # If not paused, run the cycle
                run_cycle(directions, total_iter_num)
                total_iter_num += 1
                break
    else:
        # Infinite iteration loop
        while True:
            while True:
                # Check stop flag
                if stop_flag.is_set():
                    print("Stopping the program...")
                    return
                
                # Check pause flag
                while pause_flag.is_set():
                    sleep(0.1)
                
                # If not paused, run the cycle
                run_cycle(directions, total_iter_num)
                total_iter_num += 1
                break


def click_history():
    """
    Provides user directions on how to format a click history file and displays mouse position.
    """
    
    ### PUT DIRECTIONS HERE IF DESIRED (I definitely don't desire it)
    
    pyautogui.displayMousePosition()


def stop_program(event):
    """
    Sets the stop flag to true, terminating the program.
    """
    
    stop_flag.set()


def toggle_pause(event):
    """
    Toggles the pause flag to pause or resume the autoclicker.
    """
    
    if pause_flag.is_set():
    
        for x in reversed(range(10)):
            print(f"Resuming in {x} seconds.")
            sleep(1)
    
        pause_flag.clear()
        print("Resumed...")
    else:
        pause_flag.set()
        print("Paused...")


def main():
    """
    Main function to run the autoclicker program.
    """
    
    # Check if command-line arguments are provided
    if len(sys.argv) == 1:
        # No arguments provided, show instructions and display coordinates
        click_history()
    elif len(sys.argv) == 3:
        # Two arguments provided: filename and iterations
        filename = sys.argv[1]
        try:
            iterations = int(sys.argv[2])
            follow_clicks(filename, iterations)
        except ValueError:
            print("Error: The number of iterations must be an integer.")
    else:
        print("Error: Please provide either 0 or 2 command-line arguments.")
        print("Usage: python script.py <click history filename> <number of iterations>")


if __name__ == "__main__":
    main()
