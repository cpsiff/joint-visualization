import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import csv

# if NUM_FRAMES is longer than file, whole file will be read
NUM_FRAMES = 100000
SOURCE_FILE = "data/matching_gif.csv"
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

# get list of bodies that appear in csv, set comprehension eliminates duplicates
bodies = list({int(inp[i][1]) for i in range(frames)})

# initialize dictionaries for storing body data
for body in bodies:
    data[body] = {}
    for joint in joints:
        data[body][joint] = {}
        data[body][joint]['x'] = {}
        data[body][joint]['y'] = {}
        data[body][joint]['z'] = {}

# iterate through csv, placing data in 'data' dict
# data is only stored in data[cur_body][joint][x/y/z][i] if the body appears in the ith frame
cur_frame = 1
line = 0
while line < len(inp):
    if line > 1:
        if (inp[line][0] != inp[line-1][0]):
            cur_frame += 1
    cur_body = int(inp[line][1])
    for joint in joints:
        data[cur_body][joint]['x'][cur_frame] = float(inp[line][3*joints.index(joint)+2])
        data[cur_body][joint]['y'][cur_frame] = float(inp[line][3*joints.index(joint)+3])
        data[cur_body][joint]['z'][cur_frame] = float(inp[line][3*joints.index(joint)+4])
    line += 1

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
    for body in bodies:
        joint_x += data[body][joint]['x'].values()
        joint_y += data[body][joint]['y'].values()
        joint_z += data[body][joint]['z'].values()

# find the max min and midpoints of data in each direction to neatly fit screen
maxrange = int(max(max(joint_x)-min(joint_x),max(joint_y)
           -min(joint_y),max(joint_z)-min(joint_z)))
x_midpoint = (min(joint_x) + max(joint_x)) / 2
y_midpoint = (min(joint_y) + max(joint_y)) / 2
z_midpoint = (min(joint_z) + max(joint_z)) / 2

# animate function is scheduled once per FRAME_TIME
def animate(i):
    i = i%cur_frame # so that animation loops
    ax.clear() # clear previous frame's data
    ax.set_xlim3d(x_midpoint-maxrange/2, x_midpoint+maxrange/2)
    ax.set_ylim3d(z_midpoint-maxrange/2, z_midpoint+maxrange/2)
    ax.set_zlim3d(y_midpoint-maxrange/2, y_midpoint+maxrange/2)

    # scatter plot joints (commented out) and line plot bones
    for body in bodies:
        if i in data[body]['head']['x']:
            # for joint in joints:
            #     ax.scatter(data[body][joint]['x'][i], data[body][joint]['z'][i], data[body][joint]['y'][i])
            for bone in bones:
                plt.plot([data[body][bone[0]]['x'][i],data[body][bone[1]]['x'][i]],
                        [data[body][bone[0]]['z'][i],data[body][bone[1]]['z'][i]],
                        [data[body][bone[0]]['y'][i],data[body][bone[1]]['y'][i]])

# schedule animation function
ani = animation.FuncAnimation(fig, animate, interval=FRAME_TIME)

plt.show()
