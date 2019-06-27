import csv
import os
from math import sqrt
import collections
import numpy as np

DATA_DIRECTORY = 'data/capture_converted_trimmed'

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


def distance(x1,y1,z1,x2,y2,z2):
	return sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

data_files = [DATA_DIRECTORY + '/' + f for f in os.listdir(DATA_DIRECTORY)]

print('Processing', len(data_files), 'files')

avg_stds = {}
for data_file in data_files:
    inp = list(csv.reader(open(data_file)))

    data = {}

    # initialize dictionaries for storing body data
    for joint in joints:
        data[joint] = {}
        data[joint]['x'] = []
        data[joint]['y'] = []
        data[joint]['z'] = []

    # iterate through csv, placing data in 'data' dict
    # data is only stored in data[cur_body][joint][x/y/z][i] if the body appears in the ith frame
    for i in range(len(inp)):
        for joint in joints:
            data[joint]['x'].append(float(inp[i][3*joints.index(joint)+2]))
            data[joint]['y'].append(float(inp[i][3*joints.index(joint)+3]))
            data[joint]['z'].append(float(inp[i][3*joints.index(joint)+4]))

    bone_distances = []
    for bone in bones:
        distances = []
        for i in range(len(data['head']['x'])):
            distances.append(distance(data[bone[0]]['x'][i],data[bone[0]]['y'][i],data[bone[0]]['z'][i],
                                    data[bone[1]]['x'][i],data[bone[1]]['y'][i],data[bone[1]]['z'][i]))
        bone_distances.append(distances)

    std = [np.std(d) for d in bone_distances]
    avg_std = sum(std) / len(std)
    print('file:', data_file, 'avg_std:', avg_std)
    avg_stds[data_file] = [avg_std, len(inp)]

sorted_by_value = sorted(avg_stds.items(), key=lambda kv: kv[1])

sorted_lists = [list(x) for x in sorted_by_value]
sorted_flat_lists = []
for x in sorted_lists:
    sorted_flat_lists.append([x[0],x[1][0],x[1][1]])

with open('standard_deviations_sorted.csv', 'w', newline='') as output_file:
    wr = csv.writer(output_file)
    wr.writerows(sorted_flat_lists)
