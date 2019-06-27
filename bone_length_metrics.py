import matplotlib.pyplot as plt
from pylab import *
import csv
import os
from math import sqrt
import numpy as np

#SOURCE_FILE = 'data/field_data/joint-2019-06-14-20-43-00-006__TO__joint-2019-06-14-20-43-00-006-2.csv'
SOURCE_FILE = 'data/capture_converted_trimmed/joint-2019-06-14-19-47-00-034__TO__joint-2019-06-14-19-56-00-005-158.csv'
NEIGHBORHOOD_SIZE = 25

joints = ["head","shoulderspine","leftshoulder","leftelbow","lefthand",
		"rightshoulder","rightelbow","righthand","midspine","basespine",
		"lefthip","leftknee","leftfoot","righthip","rightknee","rightfoot",
		"leftwrist","rightwrist","neck"]

# bones = [["head","shoulderspine"],["shoulderspine","neck"],["neck","midspine"],
# 		["midspine","basespine"],["shoulderspine","rightshoulder"],
# 		["rightshoulder","rightelbow"],["rightelbow","rightwrist"],
# 		["rightwrist","righthand"],["shoulderspine","leftshoulder" ],
# 		["leftshoulder", "leftelbow" ],["leftelbow", "leftwrist" ],
# 		["leftwrist", "lefthand" ],["basespine","righthip"],
# 		["righthip","rightknee"],["rightknee","rightfoot"],
# 		["basespine","lefthip" ],["lefthip", "leftknee" ],
# 		["leftknee", "leftfoot" ]]

bones = [["shoulderspine","rightshoulder"],
		["rightshoulder","rightelbow"],["rightelbow","rightwrist"],
		["rightwrist","righthand"],["shoulderspine","leftshoulder" ],
		["leftshoulder", "leftelbow" ],["leftelbow", "leftwrist" ],
		["leftwrist", "lefthand" ]]

def distance(x1,y1,z1,x2,y2,z2):
	return math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

inp = list(csv.reader(open(SOURCE_FILE)))

# initialize dictionary to store joint data from csv
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

for i in range(len(bones)):
	print(bones[i], ":", std[i])
print('Average standard deviation', avg_std)

all_neighborhood_stds = []
for i in range(len(bone_distances)):
	neighborhood_stds = []
	for j in range(len(bone_distances[i])):
		start_index = max([0,j-NEIGHBORHOOD_SIZE])
		end_index = min([len(bone_distances[i]),j+NEIGHBORHOOD_SIZE])
		neighborhood_stds.append(np.std(bone_distances[i][start_index:end_index]))
	all_neighborhood_stds.append(neighborhood_stds)

mean_std = []
for i in range(len(all_neighborhood_stds[0])):
	mean_std.append(sum([x[i] for x in all_neighborhood_stds])/len(all_neighborhood_stds))

fig = plt.figure(figsize=(8,8))
mean_std_plot = fig.add_subplot(311)
std_plot = fig.add_subplot(312)
distance_plot = fig.add_subplot(313)

mean_std_plot.plot(mean_std)

for bone in all_neighborhood_stds:
	std_plot.plot(bone)

for bone_distance in bone_distances:
	distance_plot.plot(bone_distance)

for i in range(len(mean_std)):
	if mean_std[i] > 50:
		mean_std_plot.axvspan(i,i+1, facecolor='r', alpha=0.3)
		std_plot.axvspan(i,i+1, facecolor='r', alpha=0.3)
		distance_plot.axvspan(i,i+1, facecolor='r', alpha=0.3)
	elif mean_std[i] < 18:
		mean_std_plot.axvspan(i,i+1, facecolor='g', alpha=0.3)
		std_plot.axvspan(i,i+1, facecolor='g', alpha=0.3)
		distance_plot.axvspan(i,i+1, facecolor='g', alpha=0.3)

mean_std_plot.set(ylabel='Mean Neighborhood Std. Dev.')
std_plot.set(ylabel='Neighborhood Std. Dev.')
distance_plot.set(ylabel='Bone Length')
distance_plot.set(xlabel='Frame Number')

plt.show()
