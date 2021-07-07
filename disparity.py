#!/usr/bin/env python
# coding: utf8

""" Diversity - balance. """

from typing import List, Dict, Tuple
import csv
import numpy as np
import pandas as pd
from scipy.stats import entropy
from collections import Counter
from pygini import gini
import seaborn as sns
from matplotlib import pyplot as plt
from collections import Counter

from scripts.import_data import *   


# load user fav songs
users_songs = {}
with open('../data/10K_user_fav_songs.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if i > 0:
            if row[0] in users_songs:
                users_songs[row[0]].append(row[1])
            else:
                users_songs[row[0]] = [row[1]]

# load songs tags                
songs_tags = {}         
with open('../data/10K_user_fav_songs_tags.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if row[1] == 'decade':
            if i > 0:
                if row[0] in songs_tags:    
                    if row[1] in songs_tags[row[0]]:
                        songs_tags[row[0]][row[1]].append(row[2])
                    else:
                        songs_tags[row[0]][row[1]] = [row[2]]
                else:
                    songs_tags[row[0]] = {row[1]: [row[2]]}

# keep only the oldest decade
all_decades = np.array(['20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s', '00s', '10s', '2020s'])
for song_id, tags in songs_tags.items():
    if 'decade' in tags:
        if len(songs_tags[song_id]['decade']) > 1:
            l = songs_tags[song_id]['decade']
            songs_tags[song_id]['decade'] = l[np.argmin([np.argwhere(all_decades == d)[0][0] for d in l])]
        songs_tags[song_id]['decade'] = np.argwhere(all_decades == songs_tags[song_id]['decade'])[0]
                

with open('../data/10K_user_fav_songs_ranks.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if i > 0:
            if row[1] != '' and row[1] != '0':
                if row[0] in songs_tags:
                    songs_tags[row[0]]['rank'] = int(row[1])
                else:
                    songs_tags[row[0]] = {'rank': int(row[1])}
                    
                   
# lists of user's decades
disparity = {}

for user_id, songs in users_songs.items():
    disparity[user_id] = [0, 0]
    decades = []
    ranks = []
    for song_id in songs:
        if song_id in songs_tags:
            if 'decade' in songs_tags[song_id]:
                decades.extend(songs_tags[song_id]['decade'])
            if 'rank' in songs_tags[song_id]:
                ranks.append(songs_tags[song_id]['rank'])
            
    decades = Counter(decades)
    if len(decades) <= 1:
        disparity[user_id][0] = 0
    else:
        decades = [k for k, v in sorted(decades.items(), key=lambda item: item[1])]
        disparity[user_id][0] = abs(decades[len(decades)-1] - decades[len(decades)-2])    
        
    if len(ranks) <= 1:
        disparity[user_id][1] = 0
    else:
        disparity[user_id][1] = np.max(ranks) - np.min(ranks)


df = pd.DataFrame.from_dict(disparity, orient='index', columns=['decades', 'ranks'])
df.to_csv('results/10k_disparity.csv')  

sns.histplot(data=df, x="decades")
plt.savefig('figures/disparity_decades.png')
plt.close()

sns.histplot(data=df, x="ranks")
plt.savefig('figures/disparity_ranks.png')
plt.close()


        
        



