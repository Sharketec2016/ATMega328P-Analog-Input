'''
Title: Read Serial Input from MCU
Author: Matthew Buchkowski 
Date: September 3, 2024

Description:
    The purpose of this file is to be coupled with the main.cpp firmware file for reading in analog values on ATMega328P on Arduino Nano. 
    The nano sends packets of information that are grabbed and decoded on computer. A plot is initalized and updated concurrently with new data points.
    A function for serial communication is needed as well before listening and grabbing data packets. 
    
    If the "singleCapture" is true, then it will signal capture one waveform for you and await for user input before continuing forward for another capture. 


ToDo: 
    Build a buffer such that the plot is not continously updating with new values and appending the plot, but plotting one signal at a time. Define a specified width
    that the signal must fit within and then fill that window with values. 
    
    - Also include functionality into the window to enable single shot or continous run.

'''



import serial.tools.list_ports
import matplotlib.pyplot as plt
import matplotlib as mt
from math import pow, log
import numpy as np
from time import time, sleep
mt.use("TkAgg")

singleCapture = False

def decodPacket(packet):
    """
    Take in the packet of data sent from the MCU/Peripherial, decode, and grab the voltage value. Note, this packet of data was designed with specific format, so grabbing voltage is hard coded.
    """
    strData = packet.decode("utf").rstrip('\n')
    voltage = float(strData.split()[-1])
    return voltage

def initPlot():
    '''
    Initialize the plot that will be used for displaying the change in temperature over time
    '''
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    line1, = ax.plot(0, 0)
    return fig, ax, line1


def plotAnalogSignal(valsList, fig, lsax):
    '''
    Plot the given values over time. This plot takes in a valsList that is continously increasing in time with size. Thus the plot itself will increase in plotted values and size as well, until specific by a wait timer. 
    '''
    ax = lsax
    ax.cla()
    ax.plot(np.linspace(-5, 5, len(valsList)), valsList, 'r*-')
    
    ax.set_ylim(bottom=-2, top=7)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Voltage (V)")

    fig.canvas.draw()
    fig.canvas.flush_events()
    
    


def serialInit():
    serialInst = serial.Serial()
    serialInst.baudrate = 115200
    serialInst.port = "/dev/ttyUSB1"
    serialInst.open()
    return serialInst


def main():
    print("Step 1")
    serialInst = serialInit()
    print("Step 2")
    
    valsList = np.array([])
    timesList = np.array([])
    farenhiteList = np.array([])

    fig, ax, line1 = initPlot()
    start_time = time()
    print("Step 3")
    while(True):
        # while len(valsList) < 212:
        packet = None
        print("Step 4")
        if serialInst.in_waiting:
            packet = serialInst.readline()
        print("Step 5")
        if packet:
            
            valsList = np.append(valsList, decodPacket(packet))
            # if (time() - start_time) >= 1.0:
            #     print(valsList)
            #     print(len(valsList))
            #     input("Wait")
            
        if len(valsList) == 20:
            
            plotAnalogSignal(valsList=valsList, fig=fig, lsax=ax)
            valsList = np.array([])
            if singleCapture:
                input("Waiting for continuation")
        
        



    
if __name__ == '__main__':
    main()

