# -*- coding: utf-8 -*-
"""
This program was created for the purposes of education for the Physics 4ABL 
courses offered by UCLA's Physics and Astronomy Department.
You may use/alter this program for any purpose.

@author: Javier Carmona, UCLA Department of Physics and Astronomy
                         UCLA Department of Electrical and Computer Engineering
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox
import serial

initialText = '"my_data_"'

fig = plt.figure(figsize=(20,10))

ax = plt.axes(xlim=(0, 511), ylim=(0, 65355))
ax.set_xlabel('Data Points')
ax.set_ylabel('Raw Data')
ax.set_title('Arduino Oscilloscope')
line, = ax.plot([], [], lw=2)

class AnalogPlot:
    fileIdx = 0
    saveStatus = False
    saveSwitch = True
    pressIdx = 0
    sampleInput = serial.Serial("/dev/ttyACM0", 115200, timeout = 5) 
    parentFileName = "my_data_"
    
    buffSize = 512
    inBuf = [0]*buffSize
    t = np.linspace(0, 511, buffSize)
    
    dataBuf = []

    def init(self):
        self.line.set_data([], [])
        return line,
    
    def fileNameSubmit(self, text):
        self.parentFileName = eval(text)
        
    def bufferSize(self, size):
        self.buffSize = eval(size)   
        self.inBuf = [0]*self.buffSize 
#        print(len(self.inBuf))
        self.t = np.linspace(0, self.buffSize-1, self.buffSize)
#        print(len(self.t))
        ax = plt.axes(xlim=(0, self.buffSize-1), ylim=(0, 65355))
        
        
    def saveData(self, saveStatus):
        self.pressIdx = self.pressIdx + 1
        
        if (self.pressIdx % 2 == 0):
            self.saveStatus = self.saveStatus
            self.saveSwitch = not self.saveSwitch
        else:
            print("Saving data...")
            self.saveSwitch = not self.saveSwitch
            self.saveStatus = not self.saveStatus

        
    def dataLoop(self):
        
        if (self.saveStatus == False):
            for i in range(0,self.buffSize):
                self.inBuf[i] = ((ord(self.sampleInput.read()) << 8)) | ord(self.sampleInput.read())
    #        print(self.saveStatus)
        else:
           for i in range(0,self.buffSize):
                    self.inBuf[i] = ((ord(self.sampleInput.read()) << 8)) | ord(self.sampleInput.read())
           self.dataBuf = np.append(self.dataBuf, self.inBuf)
        
        if (self.saveSwitch == True  and self.saveStatus == True):
            self.dataFileName = self.parentFileName +str(self.fileIdx) + ".csv"
            self.fileIdx = self.fileIdx + 1
            np.savetxt(self.dataFileName, self.dataBuf, delimiter=",")
            print("Done saving data. Saved under the name: " + self.dataFileName + ".")
            self.saveStatus = not self.saveStatus
            self.dataBuf = []
            
            
        return self.inBuf,
            
    def dataSet(self, analogData):
        self.analogData = self.dataLoop()
        line.set_data(self.t, self.analogData)
        return line,
        
    def printData(self, data):
        self.data = self.dataLoop()
        print(self.data)
        
    def serialClose(self, sampleInput):
        self.sampleInput.flush()
        self.sampleInput.close()    
        print("Serial port has closed.")
    
    
#
#def saveSwitch(saveStatus):
##    saveStatus = not saveStatus
#    print(saveStatus)
    
callBack = AnalogPlot()    

anim = animation.FuncAnimation(fig, callBack.dataSet, interval=33, blit=True)

axPrint = plt.axes([0.925, 0.5, 0.075, 0.05])
buttonPrint = Button(axPrint, 'Print')
buttonPrint.on_clicked(callBack.printData)

axClose = plt.axes([0.925, 0.4, 0.075, 0.05])
buttonClose = Button(axClose, 'Close')
buttonClose.on_clicked(callBack.serialClose)

axSave = plt.axes([0.925, 0.6, 0.075, 0.05])
buttonSave = Button(axSave, 'Save')
buttonSave.on_clicked(callBack.saveData)

axBox = plt.axes([0.7, 0.9, 0.2, 0.05])
fileNameBox = TextBox(axBox, 'File Name', initial = initialText)
fileNameBox.on_submit(callBack.fileNameSubmit)

axBuffer = plt.axes([0.8, 0.025, 0.1, 0.05])
bufferBox = TextBox(axBuffer, 'Buffer Size', initial = "512")
bufferBox.on_submit(callBack.bufferSize)

plt.show()
