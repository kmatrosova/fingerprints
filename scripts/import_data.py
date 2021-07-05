#!/usr/bin/env python
# coding: utf8

""" Import data from csv. """

from typing import List, Dict, Tuple

import csv
import numpy as np

def get_data_from_csv(filename: str):
    
    big_likes = []
    big_users = []
    big_items = []

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 0:
                big_likes.append([row[0], row[1]])
                big_users.append(row[0])
                big_items.append(row[1]) 
    
    big_users = np.unique(big_users).tolist()

    big_items = np.unique(big_items).tolist()
    
    print('Data was imported with success.')
    print('\nNumber or likes:', len(big_likes))
    print('\nNumber or users:', len(big_users))
    print('\nNumber or items:', len(big_items))
    return big_likes, big_users, big_items


def get_macro_tags_from_csv(filename: str):
    
    items_genre = {}
    items_rank = {}

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 0:
                if row[1] != '':
                    items_genre[row[0]] = row[1]
                    items_rank[row[0]] = row[2]
                else:
                    items_genre[row[0]] = 'unknown'
                    items_rank[row[0]] = 'unknown'
    
    print('Items info was imported with success.')
    return items_genre, items_rank

def get_detailed_tags_from_csv(filename: str, tag_type):
    
    tags = {}

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 0:
                if row[1] == tag_type:
                    if row[0] in tags:
                        tags[row[0]].append(row[2])
                    else:
                        tags[row[0]] = [row[2]]
                        
    print('Detailed tags were imported with success.')
    return tags


def get_item_name_from_csv(filename: str):
    names = {}

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 0:
                names[row[0]] = [row[2]]
                        
    print('Detailed tags were imported with success.')
    return names


def get_decades_from_csv(filename: str):
    decades = np.array(['20s', '30s', '40s', '50s', '60s', '70s', '80s', '90s', '00s', '10s', '2020s'])
    all_decades = {}

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 0:
                if row[1] == 'decade':
                    if row[0] in all_decades:
                        all_decades[row[0]].append(row[2])
                    else:
                        all_decades[row[0]] = [row[2]]
    res = {}
    for k, v in all_decades.items():
        oldest_decade = v[np.argmin([np.argwhere(decades == d)[0][0] for d in v])]
        res[k] = oldest_decade
                        
    print('Decades were imported with success.')
    return res
    
    