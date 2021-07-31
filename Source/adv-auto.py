import pyautogui
import keyboard
import threading
import os
from time import sleep
# imports needed packages


def run_cycle(directions):  # runs a single slick cycle
    for direction in directions:
        pyautogui.click(x=int(direction[0]), y=int(direction[1]))
        sleep(float(direction[2]))


def follow_clicks(filename):  # initiates click cycle loop
    f = open(filename, "r")
    directions = f.readlines()
    f.close()
    # reads click history file

    direction_list = []

    for direction in directions:  # formats click directions from file into a list
        line_list = direction.split()
        direction_list.append(line_list)

    print("\nOPERATION:")
    print(direction_list)

    iter_num = input("\nHow many times would you like to repeat this operation?  Enter any non-numerical character(s) for infinity.\n")
    # gets loop information from user

    input('\nPress ENTER to start countdown to program initiation.  After pressing, the program will commence in 10 seconds.  Press "Q" to quit.\n')

    threading.Thread(target=keyboard.on_press_key("q", lambda _: os._exit(1)))
    # starts a thread that will check for when the user clicks the "Q" key, and then and the program

    for countdown in range(10):  # intiates a 10 second countdown before code executes
        print(10 - countdown)
        sleep(1)

    if iter_num.isnumeric():  # if the user entered a number before, a for loop is opened
        iter_num = int(iter_num)

        for _ in range(iter_num):
            run_cycle(direction_list)

    else:  # if the user did not enter a number, the program loops infinitely
        while True:
            run_cycle(direction_list)


def click_history():  # gives user directions on how to format a click history file, and shows mouse position
    print("DIRECTIONS --\nCreate a new text file in the same folder as the main program.  Then format each line as follows:\nmouse-x mouse-y wait-time.\n\nExample --\n100 100 2\n50 50 1\n150 10 0\n\nIn the above example, the computer clicks at x-100 y-100 then waits 2 seconds, clicks at x-50 y-50, then waits 1 second, then clicks at x-150 y-10, then waits 0 seconds.\n\nUse the mouse location indicator below to help create this file:")
    pyautogui.displayMousePosition()


print("Advanced Programmable Autoclicker\n\n")

setup = input(f"Do you have a pre-existing click history file?  (Y/N)\n")

if setup.upper() == "N":  # manages click history file setup
    click_history()
elif setup.upper() != "Y":
    print(f"Error: Assuming file is complete")

filename = input("Enter the click history file name you would like to use\n")

try:  # makes sure file name is valid then runs the program
    follow_clicks(filename)
except:
    print("Error: Make sure the file name you are using is correct")