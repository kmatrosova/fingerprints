#!/usr/bin/env python
# coding: utf8

import pandas as pd

def macro_tags(likes, items_genres, genres):
    all_items = [i for u, i in likes]
    items_df = pd.Series(all_items, dtype='string', name='item').to_frame()
    items_genres_df = pd.DataFrame.from_records(items_genres, columns=['item', 'genre'])
    df = pd.merge(items_df, items_genres_df, on='item')
    genres_count = df.value_counts('genre')
    vector = []
    for g in genres:
        vector.append(genres_count[g] / len(likes))

    return vector