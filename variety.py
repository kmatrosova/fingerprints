#!/usr/bin/env python
# coding: utf8

""" Diversity - variety. """

from typing import List, Dict, Tuple
import csv
import numpy as np
import pandas as pd

import seaborn as sns
from matplotlib import pyplot as plt

from scripts.import_data import *   

user_songs = {}
with open('../data/10K_user_fav_songs.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if i > 0:
            if row[0] in user_songs:
                user_songs[row[0]].append(row[1])
            else:
                user_songs[row[0]] = [row[1]]


            
song_tags = {}
with open('../data/10K_user_fav_songs_tags.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if i > 0:
            if row[0] in song_tags:
                if row[1] in song_tags[row[0]]:
                    song_tags[row[0]][row[1]].append(row[2])
                else:
                    song_tags[row[0]][row[1]] = [row[2]]
            else:
                song_tags[row[0]] = {row[1]: [row[2]]}              
                
decades_list = np.array(['20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s', '00s', '10s', '2020s'])
user_vectors = {}
# go through the users
for user, items in user_songs.items():
    lang = []
    genres = []
    decades = []
    ranks = []
    
    for i in items:
        if i in song_tags:
            if 'lang' in song_tags[i]:
                lang.append(song_tags[i]['lang'])
            if 'genre' in song_tags[i]:
                genres.append(song_tags[i]['genre'])
            if 'decade' in song_tags[i]:
                v = song_tags[i]['decade']
                decades.append(v[np.argmin([np.argwhere(decades_list == d)[0][0] for d in v])])
                
    nb_songs = len(items)
    nb_lang = len(np.unique([item for sublist in lang for item in sublist]))
    nb_genres = len(np.unique([item for sublist in genres for item in sublist]))
    nb_decades = len(np.unique(decades)) 

    user_vectors[user] = [nb_songs, nb_decades, nb_lang, nb_genres]
    
df = pd.DataFrame.from_dict(user_vectors, orient='index', columns = ['songs', 'decades', 'languages', 'genres'])
df.to_csv('results/variety_vectors.csv')

sns.histplot(data=df, x="songs")
plt.savefig('figures/variety_songs.png')
plt.close()

sns.histplot(data=df, x="decades")
plt.savefig('figures/variety_decades.png')
plt.close()

sns.histplot(data=df, x="languages")
plt.savefig('figures/variety_languages.png')
plt.close()

sns.histplot(data=df, x="genres")
plt.savefig('figures/variety_genres.png')
plt.close()
