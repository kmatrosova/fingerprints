import csv
import copy
import numpy as np
from itertools import groupby
from operator import itemgetter
from operator import itemgetter
import networkx as nx
import random
import itertools
from itertools import chain
import statistics
import multiprocess
from statistics import mean, stdev
import collections
from import_data import get_data_from_csv
from max_flow import run_experiment
from max_flow import max_flow_min_cost
import pandas as pd
import matplotlib.pyplot as plt


# Get twins, remove all twins except one
def remove_twins_lv1(big_user_items, big_users, big_likes):

    big_user_items_str = {k: str(v) for k, v in big_user_items.items()}
    item_sets = [v for v in big_user_items_str.values()]

    duplicate_items = [item for item, count in collections.Counter(item_sets).items() if count > 1]

    twin_users = []
    for d in duplicate_items:
        twin_users.append([u for u, items in big_user_items_str.items() if items == d])

    for u in twin_users:
        for i, x in enumerate(u):
            if i > 0:
                for item in big_user_items[x]:
                    big_likes.remove([x, item])
                big_users.remove(x)
                big_user_items.pop(x)

    return big_user_items, big_users


    # Get twins, remove when card(twins) <= 2^n-1 (n being card(favs))
    def remove_twins_lv2(big_user_items, big_users, big_likes):

        big_user_items_str = {k: str(v) for k, v in big_user_items.items()}
        item_sets = [v for v in big_user_items_str.values()]

        duplicate_items = [item for item, count in collections.Counter(item_sets).items() if count > 1]

        twin_users = []
        for d in duplicate_items:
            twin_users.append([u for u, items in big_user_items_str.items() if items == d])

        for u in twin_users:
            nb_combinations = 2**len(big_user_items[u[0]]) - 1
            if len(u) > nb_combinations:
                for i, x in enumerate(u):
                    if i > 0:
                        for item in big_user_items[x]:
                            big_likes.remove([x, item])
                        big_users.remove(x)
                        big_user_items.pop(x)
            #else:
             #   print(len(u), len(big_user_items[u[0]]), nb_combinations)

        return big_user_items, big_users


        # Get twins, when card(twins) <= 2^n-1 -> remove card(twins) - 2^n-1
        def remove_twins_lv3(big_user_items, big_users, big_likes):

            big_user_items_str = {k: str(v) for k, v in big_user_items.items()}
            item_sets = [v for v in big_user_items_str.values()]

            duplicate_items = [item for item, count in collections.Counter(item_sets).items() if count > 1]

            twin_users = []
            for d in duplicate_items:
                twin_users.append([u for u, items in big_user_items_str.items() if items == d])

            for u in twin_users:
                nb_combinations = 2**len(big_user_items[u[0]]) - 1
                if len(u) > nb_combinations:
                    users_to_del = random.sample(u, k=len(u)-nb_combinations)
                    #print(len(u), len(big_user_items[u[0]]), len(u)-nb_combinations)
                    for x in users_to_del:
                        for item in big_user_items[x]:
                            big_likes.remove([x, item])
                        big_users.remove(x)
                        big_user_items.pop(x)
                #else:
                 #   print(len(u), len(big_user_items[u[0]]), nb_combinations)

            return big_user_items, big_users
