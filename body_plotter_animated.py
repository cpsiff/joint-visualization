import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import csv

SOURCE_FILE = "data/joint-2019-06-10-14-38-30-486.csv"
NUM_FRAMES = 100000
NUM_JOINTS = 19
FRAME_TIME = 133

joints = ["head","shoulderspine","leftshoulder","leftelbow","lefthand",
        "rightshoulder","rightelbow","righthand","midspine","basespine",
        "lefthip","leftknee","leftfoot","righthip","rightknee","rightfoot",
        "leftwrist","rightwrist","neck"]

bones = [["head","shoulderspine"],["shoulderspine","neck"],["neck","midspine"],
        ["midspine","basespine"],["shoulderspine","rightshoulder"],
        ["rightshoulder","rightelbow"],["rightelbow","rightwrist"],
        ["rightwrist","righthand"],["shoulderspine","leftshoulder" ],
        ["leftshoulder", "leftelbow" ],["leftelbow", "leftwrist" ],
        ["leftwrist", "lefthand" ],["basespine","righthip"],
        ["righthip","rightknee"],["rightknee","rightfoot"],
        ["basespine","lefthip" ],["lefthip", "leftknee" ],
        ["leftknee", "leftfoot" ]]

inp = list(csv.reader(open(SOURCE_FILE)))

frames = min(NUM_FRAMES, len(inp))

# initialize dictionary to store joint data from csv
data = {}

# add csv data to 'data' dict
for joint in joints:
    data[joint] = {}
    data[joint]['x'] = [float(x) for x in [inp[i][3*joints.index(joint)+2] for i in range(frames)]]
    data[joint]['y'] = [float(x) for x in [inp[i][3*joints.index(joint)+3] for i in range(frames)]]
    data[joint]['z'] = [float(x) for x in [inp[i][3*joints.index(joint)+4] for i in range(frames)]]

# initialize plot and figure
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# z and y axis are switched to make person appear upright
ax.set_xlabel('x axis')
ax.set_ylabel('z axis')
ax.set_zlabel('y axis')

# joint_x stores every x coordinate of every joint for every frame
joint_x = []
joint_y = []
joint_z = []
for joint in joints:
    joint_x += data[joint]['x']
    joint_y += data[joint]['y']
    joint_z += data[joint]['z']

# find the max min and midpoints of data in each direction to neatly fit screen
maxrange = int(max(max(joint_x)-min(joint_x),max(joint_y)
           -min(joint_y),max(joint_z)-min(joint_z)))
x_midpoint = (min(joint_x) + max(joint_x)) / 2
y_midpoint = (min(joint_y) + max(joint_y)) / 2
z_midpoint = (min(joint_z) + max(joint_z)) / 2

# animate function is scheduled once per FRAME_TIME
def animate(i):
    i = i%frames # so that animation loops
    ax.clear() # clear previous frame's data
    ax.set_xlim3d(x_midpoint-maxrange/2, x_midpoint+maxrange/2)
    ax.set_ylim3d(z_midpoint-maxrange/2, z_midpoint+maxrange/2)
    ax.set_zlim3d(y_midpoint-maxrange/2, y_midpoint+maxrange/2)

    # scatter plot joints
    for joint in joints:
        ax.scatter(data[joint]['x'][i], data[joint]['z'][i], data[joint]['y'][i])

    # line plot bones connecting joints
    for bone in bones:
        plt.plot([data[bone[0]]['x'][i],data[bone[1]]['x'][i]],
                [data[bone[0]]['z'][i],data[bone[1]]['z'][i]],
                [data[bone[0]]['y'][i],data[bone[1]]['y'][i]])

# schedule animation function
ani = animation.FuncAnimation(fig, animate, interval=FRAME_TIME)

plt.show()
