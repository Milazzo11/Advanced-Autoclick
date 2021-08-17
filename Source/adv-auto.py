import pyautogui
import keyboard
import threading
import os
from random import random
from time import sleep
# imports needed packages


def run_cycle(directions, total_iter_num):  # runs a single click cycle
    try:
        for direction in directions:
            if direction[0].isnumeric() or direction[0].upper() == "X" or direction[0].upper() == "CLICK":
                if direction[0].upper() == "CLICK":
                    del direction[0]

                if not direction[0].isnumeric():
                    dir0 = pyautogui.position()[0]
                else:
                    dir0 = int(direction[0])
                
                if not direction[1].isnumeric():
                    dir1 = pyautogui.position()[1]
                else:
                    dir1 = int(direction[1])

                dir2 = get_sleep(direction[2])
                
                pyautogui.click(x=dir0, y=dir1)
                sleep(dir2)
            elif direction[0].upper() == "PRESS":
                if direction[1][:7] == "*F[i]*:":
                    f = open(direction[1][7:], "r")
                    contents = f.readlines()
                    f.close()

                    pyautogui.press(contents[total_iter_num].rstrip("\n"))

                else:
                    pyautogui.press(direction[1])

                dir2 = get_sleep(direction[2])
                sleep(dir2)

            elif direction[0].upper() == "WRITE":
                dir2 = get_sleep(direction[2])

                if direction[1][:7] == "*F[i]*:":
                    f = open(direction[1][7:], "r")
                    contents = f.readlines()
                    f.close()

                    pyautogui.write(contents[total_iter_num].rstrip("\n"), dir2)
                else:
                    pyautogui.write(direction[1], dir2)

                dir3 = get_sleep(direction[3])
                sleep(dir3)
    except:
        print("Error: Make sure your click history file is formatted correctly\nProgram will terminate in 10 seconds.")
        sleep(10)
        os._exit(1)


def get_sleep(dir2):
    try:
        dir2 = float(dir2)
    except ValueError:
        if dir2[0].upper() == "R":
            if dir2[1:].isnumeric():
                dir2 = random() * float(dir2[1:])
            else:
                dir2 = dir2[1:]

                randlist = dir2.split("-")
                dir2 = random() * (float(randlist[1]) - float(randlist[0])) + float(randlist[0])

        else:
            dir2 = 0
    except:
        print("Error: Random number generation error\nProgram will terminate in 10 seconds.")
        sleep(10)
        os._exit(1) 
        
    return dir2


def follow_clicks(filename):  # initiates click cycle loop
    total_iter_num = 0

    f = open(filename, "r")
    directions = f.readlines()
    f.close()
    # reads click history file

    direction_list = []

    for direction in directions:  # formats click directions from file into a list
        line_list = direction.split()

        if line_list[0].upper() == "WRITE":
            while len(line_list) > 4:
                line_list[1] = line_list[1] + " " + line_list[2]
                del line_list[2]

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
            run_cycle(direction_list, total_iter_num)
            total_iter_num += 1

    else:  # if the user did not enter a number, the program loops infinitely
        while True:
            run_cycle(direction_list, total_iter_num)
            total_iter_num += 1


def click_history():  # gives user directions on how to format a click history file, and shows mouse position

    print("""
DIRECTIONS --
Create a new text file in the same folder as the main program.  To format mouse clicks, use the 
following format:
mouse-x mouse-y wait-time.

Example --
100 100 2
50 50 1
150 10 0

In the above example, the computer clicks at x-100 y-100 then waits 2 seconds, clicks at x-50 y-50, then waits 1 second, then clicks at x-150 y-10, then waits 0 seconds.
    
You can also replace the x and y mouse coordinates with simply "X" or "Y" and the current mouse position will be used.

Example --
x y 1
x 100 1
100 y 1

The first click will happen wherever the mouse is located, the second at the mouse's current x-coordinate and y-100, and the third at x-100 and the mouse's current y-coordinate.

Furthermore, although it does not affect functionality, you can add the command "CLICK" before your coordinates and wait time

Example --
CLICK 100 100 2
CLICK 50 50 1
CLICK 150 10 0

Here, the same results will be produced as from the first example.

You can also use the PRESS and WRITE commands, which use the following format:
PRESS key wait-time
WRITE text interval-between-letters wait-time.

Example --
PRESS ENTER 1
WRITE hello 0.5 1

In the above example, the computer presses the ENTER key, waits 1 second, types the text "hello" with a 0.5 second wait time between letters, then waits another second.

Keep in mind, when using the WRITE command, you can type spaces in your text and the program will still understand what it is supposed to do.  For example --
WRITE hello world 0.5 1

The above example would result in the text "hello world" being typed.

You can also substitute any wait time for a random number between 2 intevals.  Just type "R" then the upper random limit, or "R" followed by the lower random limit, a "-" and then the upper random limit.

Example --
100 100 r1
50 200 r4-10

The first line will wait between 0 and 1 seconds after clicking, and the second line will wait between 4 and 10 seconds.

you can use the mouse location indicator below to help create your click history file:""")
# prints the program directions

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