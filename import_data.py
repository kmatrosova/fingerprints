# %%
import csv
import numpy as np
from itertools import groupby
from operator import itemgetter

# %%
def get_data_from_csv(filename):
    
    big_likes = []
    big_users = []
    big_items = []

    with open(filename, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            big_likes.append(row)
            big_users.append(row[0])
            big_items.append(row[1])

    big_users = np.unique(big_users).tolist()

    big_items = np.unique(big_items).tolist()

    big_user_items = {user: list(list(zip(*item))[1]) for user, item in groupby(big_likes, itemgetter(0))}

    big_item_users = {item: list(list(zip(*user))[0]) 
                      for item, user in groupby(sorted(big_likes, key=itemgetter(1)), itemgetter(1))}
    
    print('Data was imported with success.')
    return big_likes, big_users, big_items, big_user_items, big_item_users
    

# %%
