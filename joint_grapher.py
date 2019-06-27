import matplotlib.pyplot as plt
from pylab import *
import csv
import os

NUM_FRAMES = 45
NUM_JOINTS = 19
joints = ["Head","ShoulderSpine","LeftShoulder","LeftElbow","LeftHand","RightShoulder","RightElbow","RightHand","MidSpine","BaseSpine","LeftHip","LeftKnee","LeftFoot","RightHip","RightKnee","RightFoot","LeftWrist","RightWrist","Neck"]

fig = plt.figure(figsize=(8,8))
myPlots = []
myPlots.append(fig.add_subplot(311))
myPlots.append(fig.add_subplot(312))
myPlots.append(fig.add_subplot(313))

data = list(csv.reader(open("data/capture_converted_trimmed/joint-2019-06-14-19-47-00-034__TO__joint-2019-06-14-19-56-00-005-158.csv")))

t = [x for x in range(NUM_FRAMES)]

offset = 2
for myPlot in myPlots:
    for x in range(NUM_JOINTS):
        toPlot= []
        for i in range(NUM_FRAMES):
            toPlot.append(float(data[i][(x*3)+offset]))

        myPlot.plot(t, toPlot, label=str(joints[x]))

    plt.xlabel('Frame number')
    offset += 1

myPlots[0].set(ylabel='x coordinate')
myPlots[1].set(ylabel='y coordinate')
myPlots[2].set(ylabel='z coordinate')
plt.legend(bbox_to_anchor=(1.05, 3), loc=2, borderaxespad=0)
matplotlib.pyplot.subplots_adjust(right=0.75)
plt.show()
