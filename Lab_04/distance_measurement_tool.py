# Written by Savindu9x
# Last Modified on 18-09-2021
# Import required libraries
import RPi.GPIO as GPIO
import csv
import tkinter as tk
from tkinter import Tk, Label, Entry, Button
import random
# Importing the Kmeans cluster algorithm GUI module
# prepared in the lab activity 02
from gui_output import kmeansProcess

#Set GPIO pins for ultrasonic sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
PIN_TRIGGER = 18
PIN_ECHO = 16
GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

# Loads the distance measurement gui window
def loadInterface():
    # Initialize Global variables
    global save_array
    # Setting up the tkinter window
    root = Tk()
    root.title('Distance Measurement tool')
    canvas1 = tk.Canvas(root, width=350, height=250, relief='raised')
    canvas1.pack()
    #Textbox for number of data points
    label1 = Label(root, text="Specify Number of data points: ")
    canvas1.create_window(175, 25, window=label1)
    label1.config(font=('helvetica', 10))
    # Box to Enter the number of data points
    entry1 = Entry(root)
    canvas1.create_window(175, 50, window=entry1)
    # returns measured distance in two decimal points
    # has a two second delay of reading sensor data
    def calculateDistance():
        print("Waiting for sensor to settle\n")
        time.sleep(1)
        print("Calculating distance")
        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        while GPIO.input(PIN_ECHO) == 0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        print("Distance:", distance, "cm")
        return distance
    # function to append data to existing excel file
    def saveFile(save_array,n):
        # opens an existing .csv file and pass as a file object
        if n == 0:
            # For clear button, list objects are deleted.
            del save_array[:]
            # Lets the user know with a message.
            print("\nList is Reset")
        else:
            # Lets the user know process has been executed.
            print("\nData Array is saved to lab4_dataset.csv")
            with open('lab4_dataset.csv', 'a', newline='') as f:
                # returns writer object to convert user data into delimited strings.
                write = csv.writer(f)
                # Write all elements in rows to the writer’s file object
                write.writerows(save_array)

    def gatherData():
        # gets the user input data points length
        num_data_points = int(entry1.get())
        # Resets the distance array to get new dataset
        dist_array = []
        # Iterated to Number specified by the user for collection
        for iter in range(num_data_points):
            # returns measured distance
            dist = calculateDistance()
            # Append each distance to the list
            dist_array.append(dist)
        # Passing array of measured distances to a list of lists
        save_array.append(dist_array)
        print(save_array)
        # Let user know sample collection is finished and
        # gives him a interval to prepare for next sample collection
        print("One sample is finished collecting.\nGet ready for next sample")
    # Creating a button to measure the distance
    measureButton = Button(text="Measure", command=lambda: gatherData(), bg='green', fg='white',
                               font=('helvetica', 12, 'bold'))
    canvas1.create_window(175, 80, window=measureButton)
    # Creating a button to export the distance data
    saveButton = Button(text="Export", command=lambda: saveFile(save_array,1), bg='blue', fg='white',
                         font=('helvetica', 12, 'bold'))
    canvas1.create_window(175, 120, window=saveButton)
    # Creating a button to clear the current distance data
    clearButton = Button(text="Clear", command=lambda: saveFile(save_array,0), bg='red', fg='white',
                           font=('helvetica', 12, 'bold'))
    canvas1.create_window(175, 160, window=clearButton)
    root.mainloop()
# Initiate lists for collecting
# distances and saving data to csv file
save_array = []
def main():
    loadInterface()
    print("Ok")
    # This file contains GUI for exporting .xls file
    # processing of Kmeans algorithm which demonstrated in activity 02
    kmeansProcess()
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

