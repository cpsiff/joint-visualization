import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
from pylab import *
import csv
import os

NUM_FRAMES = 100000
NUM_JOINTS = 19
joints = ["head","shoulderspine","leftshoulder","leftelbow","lefthand",
        "rightshoulder","rightelbow","righthand","midspine","basespine",
        "lefthip","leftknee","leftfoot","righthip","rightknee","rightfoot",
        "leftwrist","rightwrist","neck"]


userin = input("What joint would you like to plot:")
while(userin.lower() not in joints):
    print("Please enter a valid joint")
    userin = input("What joint would you like to plot:")

data = list(csv.reader(open("joint-2019-06-10-14-38-30-486.csv")))

frames = min(NUM_FRAMES, len(data))
joint_x = [float(x) for x in [data[i][3*joints.index(userin.lower())+2] for i in range(frames)]]
joint_y = [float(y) for y in [data[i][3*joints.index(userin.lower())+3] for i in range(frames)]]
joint_z = [float(z) for z in [data[i][3*joints.index(userin.lower())+4] for i in range(frames)]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# z and y axis are switched when rendering for more intuitive display
ax.scatter(joint_x, joint_z, joint_y)
ax.set_xlabel('x axis')
ax.set_ylabel('z axis')
ax.set_zlabel('y axis')

maxrange = int(max(max(joint_x)-min(joint_x),max(joint_y)-min(joint_y),max(joint_z)-min(joint_z)))
x_midpoint = (min(joint_x) + max(joint_x)) / 2
y_midpoint = (min(joint_y) + max(joint_y)) / 2
z_midpoint = (min(joint_z) + max(joint_z)) / 2
ax.set_xlim3d(x_midpoint-maxrange/2, x_midpoint+maxrange/2)
ax.set_ylim3d(z_midpoint-maxrange/2, z_midpoint+maxrange/2)
ax.set_zlim3d(y_midpoint-maxrange/2, y_midpoint+maxrange/2)

plt.show()
