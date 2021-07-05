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
            if row[1] != '':
                if row[0] in songs_tags:
                    songs_tags[row[0]]['rank'] = int(row[1])
                else:
                    songs_tags[row[0]] = {'rank': int(row[1])}
                   
# lists of user's decades
users_decades = {}
for user_id, songs in users_songs.items():
    users_decades[user_id] = []
    for song_id in songs:
        if song_id in songs_tags:
            if 'decade' in songs_tags[song_id]:
                users_decades[user_id].extend(songs_tags[song_id]['decade'])

                
# lists of user's ranks
users_ranks = {}
for user_id, songs in users_songs.items():
    users_ranks[user_id] = []
    for song_id in songs:
        if song_id in songs_tags:
            if 'rank' in songs_tags[song_id]:
                users_ranks[user_id].append(songs_tags[song_id]['rank'])

                
# init Gini coef        
users_gini = {}
for user_id in users_songs:
    users_gini[user_id] = [0, 0]     
                
# users decades Gini coef        
for user_id, decades in users_decades.items():
    if  decades != []:
        users_gini[user_id][1] = gini(np.asarray(decades, dtype=float)) 
        
# users ranks Gini coef        
for user_id, ranks in users_ranks.items():
    if ranks != []:
        users_gini[user_id][0] = gini(np.asarray(ranks, dtype=float)) 
        

df = pd.DataFrame.from_dict(users_gini, orient='index', columns=['decades', 'ranks'])

df.to_csv('results/10k_gini.csv')  

sns.histplot(data=df, x="decades")
plt.savefig('figures/gini_decades.png')
plt.close()

sns.histplot(data=df, x="ranks")
plt.savefig('figures/gini_ranks.png')
plt.close()
