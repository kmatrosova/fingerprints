#!/usr/bin/env python
# coding: utf8

from scripts.import_data import *
from scripts.vectors import macro_tags

genres = get_tags_from_csv('../data/macro_tags.csv')
big_likes, big_users, big_items = get_data_from_csv('../data/users_bipartite_aligned_artist_1000000.csv')
items_genres, items_rank = get_macro_tags_from_csv('../data/artists_labeled.csv')
items_genres = [[k,v] for k, v in items_genres.items()]

# mean vector
mean = macro_tags(big_likes, items_genres, genres)
with open('results/mean_macro_tags.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(mean)
    
# vector for each user 
users_vectors = {}
for i, u in enumerate(big_users):
    likes = [row for row in big_likes if row[0] == u]
    users_vectors[u] = macro_tags(big_likes, items_genres, genres)
    if (i % 100 == 0):
        print(i)
    
with open('results/mean_macro_tags.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    for u, v in users_vectors:
        wr.writerow(u + ',' + v)
