import csv
import os
from math import sqrt
import collections

DATA_DIRECTORY = 'capture'

data_files = [DATA_DIRECTORY + '/' + f for f in os.listdir(DATA_DIRECTORY)]
print('Processing', len(data_files), 'files')

total_bodies_per_frame = []
null_rows = 0
for data_file in data_files:
    data = list(csv.reader(open(data_file)))
    total_frames = len({data[i][0] for i in range(len(data))})
    line = 0
    cur_frame = 1
    bodies_per_frame = [0] * (total_frames + 1)
    while line < len(data):
        if line > 0:
            if data[line][2:58] == ['0']*56:
                null_rows += 1
            elif bodies_per_frame[cur_frame] == 0:
                bodies_per_frame[cur_frame] += 1
            if (data[line][0] == data[line-1][0]):
                bodies_per_frame[cur_frame] += 1
            else:
                cur_frame += 1
        line += 1
    total_bodies_per_frame += bodies_per_frame

print('Total frames:', len(total_bodies_per_frame))
print(collections.Counter(total_bodies_per_frame))
print('Null rows:', null_rows)
