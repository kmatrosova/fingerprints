#!/usr/bin/env python
# coding: utf8

import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import plotly.figure_factory as ff
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score



from scripts.import_data import *

big_likes, big_users, big_items = get_data_from_csv('../data/my_favs/my_artists.csv')
detailed_genres = get_detailed_tags_from_csv('../data/my_favs/songs_detailed_tags.csv', 'genre')
items_lang = get_detailed_tags_from_csv('../data/my_favs/songs_detailed_tags.csv', 'lang')
items_location = get_detailed_tags_from_csv('../data/my_favs/songs_detailed_tags.csv', 'location')
items_titles = get_item_name_from_csv('../data/my_favs/my_songs.csv')
items_decades = get_decades_from_csv('../data/my_favs/songs_detailed_tags.csv')

unique_items = np.array([k for k in detailed_genres])
items_titles = [items_titles[i] for i in unique_items]
unique_genres = np.unique([item for k, sublist in detailed_genres.items() for item in sublist])


"""genre_matrix = np.zeros([len(unique_items), len(unique_genres)])

for song_id, genres in detailed_genres.items():
    for g in genres:
        genre_matrix[np.argwhere(unique_items == song_id)[0][0]][np.argwhere(unique_genres == g)[0][0]] = 1

        
# K-means
for n in range(2, 30):

    clustering = AgglomerativeClustering(n_clusters=n).fit(genre_matrix)
    labels = clustering.labels_

    res = {}
    for l in np.unique(labels):
        res[l] = []

    for i, l in enumerate(labels):
        res[l].append(items_titles[i])

    if n == 9:
        for k, v in res.items():
            print(k, v, '\n')
        
    print("Nombre de clusters: ", n, ", Silhouette score: ", silhouette_score (genre_matrix, labels, metric='euclidean'))"""
    
unique_lang = np.unique(list(items_lang.values()))
unique_loc = np.unique(list(items_location.values()))
    
lang_loc_matrix = []

for i in unique_items:
    lang = np.argwhere(unique_lang == items_lang[i][0])[0][0] if i in items_lang else -1
    loc = np.argwhere(unique_loc == items_location[i][0])[0][0] if i in items_location else -1
    lang_loc_matrix.append([lang, loc])
    
print(lang_loc_matrix)

# K-means
clustering = AgglomerativeClustering(n_clusters=4).fit(lang_loc_matrix)
labels = clustering.labels_

res = {}
for l in np.unique(labels):
    res[l] = []

for i, l in enumerate(labels):
    res[l].append(items_titles[i])


for k, v in res.items():
    print(k, v, '\n')

print(unique_lang, unique_loc)
print("Silhouette score: ", silhouette_score (lang_loc_matrix, labels, metric='euclidean'))
