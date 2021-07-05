import csv
import numpy as np
import pandas as pd
import statistics as st

data = []
data_bis = []
with open('results/count_vectors.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if i > 0:
            data.append([int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6])])

data = np.array(data)

for col in range(0, 5):
    print(min(data[:, col]), max(data[:, col]), st.mean(data[:, col]), st.stdev(data[:, col]), st.median(data[:, col]))