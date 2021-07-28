# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 08:47:31 2021

@author: Bria
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import imageio
import pandas as pd
import csv

df = pd.read_csv("position.csv")
rows, columns = (1, 1)
fig, ax = plt.subplots(rows, columns, figsize = (15,10))
#image = np.flip(image, axis=2)

i = 0
x = df["X"]
y = df["Y"]

index = len(x)
while i < index:
    #plt.clf()
    if x[i] != "X" and y[i] != "Y":
        newX = x[i]
        newY = y[i]

        plt.plot(newX, newY, 'bo')

    plt.pause(0.1)
    plt.draw()
    
    i += 1
#plt.plot(2870, 1050, marker = 'v', color = 'red')

"""
#plt.imshow()
# initializing a figure in
# which the graph will be plotted

fig = plt.figure()

# marking the x-axis and y-axis
axis = plt.axes(xlim=(0, 20),
                ylim=(0, 20))

# initializing a line variable
line, = axis.plot([], [], lw=3)

# data which the line will
# contain (x, y)


def init():
    line.set_data([], [])
    return line


def animate(i):
    while i < len(df["X"]):
        x = df["X"][i]

        # plots a sine graph
        y = df["Y"][i]

        line.set_data(x, y)
        i += 2

#    return line


anim = FuncAnimation(fig, animate, init_func=init,
                     frames=200, interval=20, blit=True)


anim.save('trial.mp4',
          writer='ffmpeg', fps=30)
"""
