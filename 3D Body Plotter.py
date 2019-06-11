import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
from pylab import *
import csv

NUM_FRAMES = 100000
NUM_JOINTS = 19
joints = ["head","shoulderspine","leftshoulder","leftelbow","lefthand",
        "rightshoulder","rightelbow","righthand","midspine","basespine",
        "lefthip","leftknee","leftfoot","righthip","rightknee","rightfoot",
        "leftwrist","rightwrist","neck"]

inp = list(csv.reader(open("joint-2019-06-10-14-38-30-486.csv")))

frames = min(NUM_FRAMES, len(inp))

data = {}

for joint in joints:
    data[joint] = {}
    data[joint]['x'] = [float(x) for x in [inp[i][3*joints.index(joint)+2] for i in range(frames)]]
    data[joint]['y'] = [float(x) for x in [inp[i][3*joints.index(joint)+3] for i in range(frames)]]
    data[joint]['z'] = [float(x) for x in [inp[i][3*joints.index(joint)+4] for i in range(frames)]]

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for joint in joints:

    ax.scatter(data[joint]['x'][0], data[joint]['z'][0], data[joint]['y'][0])

ax.set_xlabel('x axis')
ax.set_ylabel('z axis')
ax.set_zlabel('y axis')

joint_x = []
joint_y = []
joint_z = []

for joint in joints:
    joint_x += data[joint]['x']
    joint_y += data[joint]['y']
    joint_z += data[joint]['z']

maxrange = int(max(max(joint_x)-min(joint_x),max(joint_y)-min(joint_y),max(joint_z)-min(joint_z)))
x_midpoint = (min(joint_x) + max(joint_x)) / 2
y_midpoint = (min(joint_y) + max(joint_y)) / 2
z_midpoint = (min(joint_z) + max(joint_z)) / 2
ax.set_xlim3d(x_midpoint-maxrange/2, x_midpoint+maxrange/2)
ax.set_ylim3d(z_midpoint-maxrange/2, z_midpoint+maxrange/2)
ax.set_zlim3d(y_midpoint-maxrange/2, y_midpoint+maxrange/2)

plt.show()
