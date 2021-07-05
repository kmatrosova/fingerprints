#!/usr/bin/env python
# coding: utf8

""" Diversity - balance. """

from typing import List, Dict, Tuple
import csv
import numpy as np
import pandas as pd
from scipy.stats import entropy
from collections import Counter
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
            songs_tags[song_id]['decade'] = [l[np.argmin([np.argwhere(all_decades == d)[0][0] for d in l])]]
    
# lists of user's decades
users_decades = {}
for user_id, songs in users_songs.items():
    users_decades[user_id] = []
    for song_id in songs:
        if song_id in songs_tags:
            if 'decade' in songs_tags[song_id]:
                users_decades[user_id].extend(songs_tags[song_id]['decade'])

# lists of user's languages
users_languages = {}
for user_id, songs in users_songs.items():
    users_languages[user_id] = []
    for song_id in songs:
        if song_id in songs_tags:
            if 'lang' in songs_tags[song_id]:
                users_languages[user_id].extend(songs_tags[song_id]['lang'])
              
# lists of user's genres
users_genres = {}
for user_id, songs in users_songs.items():
    users_genres[user_id] = []
    for song_id in songs:
        if song_id in songs_tags:
            if 'genre' in songs_tags[song_id]:
                users_genres[user_id].extend(songs_tags[song_id]['genre'])


# init Shannon entopie        
users_entropie = {}
for user_id in users_songs:
    users_entropie[user_id] = [0, 0, 0]                
                
# users decade Shannon entopie
for user_id, decades in users_decades.items():
    users_entropie[user_id][0] = entropy([d/len(decades) for d in list(Counter(decades).values())])                
# users language Shannon entopie        
for user_id, languages in users_languages.items():
    users_entropie[user_id][1] = entropy([l/len(languages) for l in list(Counter(languages).values())])                
# users genre Shannon entopie        
for user_id, genres in users_genres.items():
    users_entropie[user_id][2] = entropy([g/len(genres) for g in list(Counter(genres).values())])

    
df = pd.DataFrame.from_dict(users_entropie, orient='index', columns=['decades', 'languages', 'genres'])

df.to_csv('results/10k_shannon.csv')  

sns.histplot(data=df, x="decades")
plt.savefig('figures/shannon_decades.png')
plt.close()

sns.histplot(data=df, x="languages")
plt.savefig('figures/shannon_languages.png')
plt.close()

sns.histplot(data=df, x="genres")
plt.savefig('figures/shannon_genres.png')
plt.close()
