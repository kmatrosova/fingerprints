import csv
import copy
import numpy as np
from itertools import groupby
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
from max_flow import max_flow_min_cost
from pretreat_twins import remove_twins_lv3


# k random items (or less)
def k_rand(big_users, big_user_items, max_items=5):

    results = []

    for power in range(2,6):

        avg_cards = []
        sum_cards = []
        ks = []

        n = 10 if power < 5 else 1

        for i in range(0,n):

            users = random.sample(big_users, k=10**power) if power < 5 else copy.copy(big_users)
            user_items = {}

            for u in users:
                if len(big_user_items[u]) <= 5:
                    user_items[u] = big_user_items[u]
                else:
                    user_items[u] = random.sample(big_user_items[u], k=max_items)

            items = np.unique(list(chain.from_iterable(list(user_items.values())))).tolist()

            likes = []
            for user, item_list in user_items.items():
                for item in item_list:
                    likes.append([user, item, 1])

            # Fingerprints

            fingerprints, sum_card, avg_card, k = max_flow_min_cost(users, items, user_items, likes)

            avg_cards.append(avg_card)
            sum_cards.append(sum_card)
            ks.append(k)

        results.append({'nb_users': 10**power,
               'avg_avg_cards': statistics.mean(avg_cards),
               'stdev_avg_cards': statistics.stdev(avg_cards) if n < 5 else 0,
               'avg_k': sum(ks) / len(ks),
               'max_k': max(ks)})

        print({'nb_users': 10**power,
               'avg_avg_cards': statistics.mean(avg_cards),
               'stdev_avg_cards': statistics.stdev(avg_cards) if n < 5 else 0,
               'avg_k': sum(ks) / len(ks),
               'max_k': max(ks)})

    return results


# k less popular items (or less)
def k_less_pop(big_users, big_user_items, max_items=5):

    results = []
    print(big_user_items[big_users[0]], big_user_items[big_users[1]], big_user_items[big_users[2]])

    big_item_users = {item: list(list(zip(*user))[0])
                      for item, user in groupby(sorted(big_likes, key=itemgetter(1)), itemgetter(1))}


    big_user_items = {u: [i for i, p in sorted([[i, len(big_item_users[i])]
                                                for i in items],
                                        key=lambda x: x[1])]
                      for u, items in big_user_items.items()}

    print(big_user_items[big_users[0]], big_user_items[big_users[1]], big_user_items[big_users[2]])

    #big_user_items = {u: (items if len(items) <= max_items else items[:max_items])
    #                  for u, items in big_user_items.items()}

    for power in range(2,6):

        avg_cards = []
        sum_cards = []
        ks = []

        n = 10 if power < 5 else 1

        for i in range(0,n):

            users = random.sample(big_users, k=10**power) if power < 5 else copy.copy(big_users)
            user_items = {}

            for u in users:
                user_items[u] = big_user_items[u] if len(big_user_items[u]) <= max_items \
                                else big_user_items[u][:max_items]
                print(u, user_items[u])
            items = np.unique(list(chain.from_iterable(list(user_items.values())))).tolist()

            likes = []
            for user, item_list in user_items.items():
                for item in item_list:
                    likes.append([user, item, 1])

            # Fingerprints

            fingerprints, sum_card, avg_card, k = max_flow_min_cost(users, items, user_items, likes)

            avg_cards.append(avg_card)
            sum_cards.append(sum_card)
            ks.append(k)

        results.append({'nb_users': 10**power,
               'avg_avg_cards': statistics.mean(avg_cards),
               'stdev_avg_cards': statistics.stdev(avg_cards) if n < 5 else 0,
               'avg_k': sum(ks) / len(ks),
               'max_k': max(ks)})

        print({'nb_users': 10**power,
               'avg_avg_cards': statistics.mean(avg_cards),
               'stdev_avg_cards': statistics.stdev(avg_cards) if n < 5 else 0,
               'avg_k': sum(ks) / len(ks),
               'max_k': max(ks)})

    return results


# k less popular items (or less) but in random order
def k_less_pop_rand(big_users, big_user_items, max_items=5):

    results = []

    big_item_users = {item: list(list(zip(*user))[0])
                      for item, user in groupby(sorted(big_likes, key=itemgetter(1)), itemgetter(1))}

    sorted_big_user_items = create_sorted_lists(big_users, big_user_items, big_item_users)


    for power in range(2,6):

        avg_cards = []
        sum_cards = []
        ks = []

        n = 10 if power < 5 else 1

        for i in range(0,n):

            users = random.sample(big_users, k=10**power) if power < 5 else copy.copy(big_users)
            user_items = {}


            for u in users:
                user_items[u] = big_user_items[u] if len(big_user_items[u]) <= max_items \
                                else pick_rand_less_pop(sorted_big_user_items[u], max_items)

            items = np.unique(list(chain.from_iterable(list(user_items.values())))).tolist()

            likes = []
            for user, item_list in user_items.items():
                for item in item_list:
                    likes.append([user, item, 1])

            # Fingerprints

            fingerprints, sum_card, avg_card, k = max_flow_min_cost(users, items, user_items, likes)

            avg_cards.append(avg_card)
            sum_cards.append(sum_card)
            ks.append(k)

        results.append({'nb_users': 10**power,
               'avg_avg_cards': statistics.mean(avg_cards),
               'stdev_avg_cards': statistics.stdev(avg_cards) if n < 5 else 0,
               'avg_k': sum(ks) / len(ks),
               'max_k': max(ks)})

        print({'nb_users': 10**power,
               'avg_avg_cards': statistics.mean(avg_cards),
               'stdev_avg_cards': statistics.stdev(avg_cards) if n < 5 else 0,
               'avg_k': sum(ks) / len(ks),
               'max_k': max(ks)})

    return results
