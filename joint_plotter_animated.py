import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import csv
import os


NUM_FRAMES = 100000
NUM_JOINTS = 19
TRAIL_LENGTH = 10
FRAME_TIME = 142
SOURCE_FILE = "data/right-arm-circles.csv"

joints = ["head","shoulderspine","leftshoulder","leftelbow","lefthand",
        "rightshoulder","rightelbow","righthand","midspine","basespine",
        "lefthip","leftknee","leftfoot","righthip","rightknee","rightfoot",
        "leftwrist","rightwrist","neck"]


userin = input("What joint would you like to plot:")
while(userin.lower() not in joints):
    print("Please enter a valid joint")
    userin = input("What joint would you like to plot:")

data = list(csv.reader(open(SOURCE_FILE)))

frames = min(NUM_FRAMES, len(data))
joint_x = [float(x) for x in [data[i][3*joints.index(userin.lower())+2] for i in range(frames)]]
joint_y = [float(y) for y in [data[i][3*joints.index(userin.lower())+3] for i in range(frames)]]
joint_z = [float(z) for z in [data[i][3*joints.index(userin.lower())+4] for i in range(frames)]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# z and y axis are switched when rendering for more intuitive display
ax.set_xlabel('x axis')
ax.set_ylabel('z axis')
ax.set_zlabel('y axis')

maxrange = int(max(max(joint_x)-min(joint_x),max(joint_y)-min(joint_y),max(joint_z)-min(joint_z)))
x_midpoint = (min(joint_x) + max(joint_x)) / 2
y_midpoint = (min(joint_y) + max(joint_y)) / 2
z_midpoint = (min(joint_z) + max(joint_z)) / 2

colors = [[0.2,0.2,1,i/TRAIL_LENGTH] for i in range(TRAIL_LENGTH)]

def animate(i):
    i = i%len(joint_x)
    anim_x, anim_y, anim_z = [],[],[]
    for j in range(i, i+TRAIL_LENGTH):
        if j >= len(joint_x):
            j = j-len(joint_x)
        anim_x.append(joint_x[j])
        anim_y.append(joint_y[j])
        anim_z.append(joint_z[j])

    ax.clear()
    ax.set_xlim3d(x_midpoint-maxrange/2, x_midpoint+maxrange/2)
    ax.set_ylim3d(z_midpoint-maxrange/2, z_midpoint+maxrange/2)
    ax.set_zlim3d(y_midpoint-maxrange/2, y_midpoint+maxrange/2)

    ax.scatter(anim_x, anim_z, anim_y, c=colors, depthshade=False)

ani = animation.FuncAnimation(fig, animate, interval=FRAME_TIME)
plt.show()
