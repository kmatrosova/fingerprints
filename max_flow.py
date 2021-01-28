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

# k among n combinations
def combinations(args):
    user, items, k = args
    return np.array([[user, '&'.join(row)] for row in list(itertools.combinations(items, k))])

def create_graph(users, items, likes):

    G = nx.DiGraph()
    G.add_nodes_from(users)
    G.add_nodes_from(items)
    G.add_nodes_from(['s', 't'])

    for u in users:
        G.add_edge('s', u, **{"capacity": 1, "weight": 1})

    for l in likes:
        G.add_edge(l[0], l[1], **{"capacity": 1, "weight": 1})

    for i in items:
        G.add_edge(i, 't', **{"capacity": 1, "weight": 1})

    return G


    def complete_graph(k, G, users, items, likes, user_items):

        try:
            # Create items combinations of size k
            pool = multiprocess.Pool()
            my_combinations = pool.map(combinations,
                                       ([user, item_list, k] for user, item_list in user_items.items()
                                        if len(item_list) >= k))
            #print(len(my_combinations), my_combinations[0], my_combinations[1], my_combinations[2])
            new_likes = []

            for i in range(0, len(my_combinations)):
                for j in range(0, len(my_combinations[i])):
                    new_likes.append([my_combinations[i][j][0], my_combinations[i][j][1], k])

            new_items = np.array(np.unique(np.array(new_likes)[:,1]))

            G.add_nodes_from(new_items, bipartite=1)

            for l in new_likes:
                G.add_edge(l[0], l[1], **{"capacity": 1, "weight": 2})

            for i in new_items:
                G.add_edge(i, 't', **{"capacity": 1, "weight": 1})

        # To make sure processes are closed in the end, even if errors happen
        finally:
            pool.close()
            pool.join()

        return G


def max_flow_min_cost(users, items, user_items, likes):
    """
        Parameters
        ----------

        Returns
        ----------

    """

    previously_covered = 0

    # Pour k allant de 1 à n?
    for k in range (1, 5):

        # Création des ensembles des items de taille allant de 1 à k
        if k == 1:
            G = create_graph(users, items, likes)

        else:
            previously_covered = len(fingerprints)
            #undefined_users = [u for u in users if u not in fingerprints.keys()]
            #print(undefined_users)
            #print([x for x in user_items.items() if x[0] in undefined_users])
            G = complete_graph(k, G, users, items, likes, user_items)

        # Calculate max flow min cost
        mincostFlow = nx.max_flow_min_cost(G, 's', 't')

        # Init fingerprints
        fingerprints = {}
        for row1 in mincostFlow.items():
            if row1[0] != 's':
                for row2 in row1[1].items():
                    if row2[0] != 't' and row2[1] != 0:
                        fingerprints[row1[0]] = row2[0]

        # Calculate sum_cards and avg_card
        sum_cards = 0

        for f in fingerprints.values():
            sum_cards += f.count('&') + 1

        avg_card = sum_cards / len(fingerprints.values())

        print('Nb fingerprints', len(fingerprints), 'Sum of fingerprints cardinals:', sum_cards, 'avg_card:', avg_card, 'k:', k)

        # If there is a fingerprint for each user - end of algorithm
        if len(fingerprints) == len(users):
            return fingerprints, sum_cards, avg_card, k

        # If the number of fingerprints did not change since the last iterration - end of algorithm
        if len(fingerprints) == previously_covered:
            return fingerprints, sum_cards, avg_card, k-1

    return fingerprints, sum_cards, avg_card, k


# From 100 to 10 000 users

def run_experiment(big_users, big_user_items):

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
                  user_items[u] = random.sample(big_user_items[u], k=5)

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

      stdev = statistics.stdev(avg_cards) if power < 5 else 0

      results.append({'nb_users': 10**power,
             'avg_avg_cards': statistics.mean(avg_cards),
             'stdev_avg_cards': stdev,
             'avg_k': sum(ks) / len(ks),
             'max_k': max(ks)})

      print({'nb_users': 10**power,
             'avg_avg_cards': statistics.mean(avg_cards),
             'stdev_avg_cards': stdev,
             'avg_k': sum(ks) / len(ks),
             'max_k': max(ks)})

  return results
