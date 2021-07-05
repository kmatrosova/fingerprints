# %%
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
from statistics import mean, stdev, median
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import plotly.graph_objects as go
from networkx import Graph
from networkx import connected_components
from scipy.optimize import curve_fit
import collections
from math import *

# %%
def info_table(big_user_items, big_item_users):
    len_big_user_items = [len(row[1]) for row in big_user_items.items()]
    len_big_item_users = [len(row[1]) for row in big_item_users.items()]

    info_table = [['min', 'max', 'mean', 'stdev', 'median'],
                  [min(len_big_user_items), max(len_big_user_items), mean(len_big_user_items), stdev(len_big_user_items), median(len_big_user_items)],
                  [min(len_big_item_users), max(len_big_item_users), mean(len_big_item_users), stdev(len_big_item_users), median(len_big_item_users)]
                 ]
    return info_table

# %%
def distribution(data):
    count_data = [len(v) for k, v in data.items()]
    distribution = {}
    for row in count_data:
        if row not in distribution:
            distribution[row] = count_data.count(row)
    return distribution

# %%
# Functions to fit power distributions

def power_law(x, a, b):
    return a*np.power(x, b)

def pareto_law(x, a, b):
    return a**(b/np.power(x, b+1))

# Fit the dummy power-law data
def simple_fit(data):
    xs = list(data.keys())
    ys = list(data.values())
    pars, cov = curve_fit(f=power_law, xdata=xs, ydata=ys, p0=[0, 0], bounds=(-np.inf, np.inf))
    return pars, xs, power_law(xs, *pars)

# Fit power-law data by log bins 
def log_fit(data, n=3):
    data = collections.OrderedDict(sorted(data.items()))
    power = 1
    fitted_xs = []
    fitted_ys = []
    coefs = []
    while n**(power-1) <= max(data.keys()):
        my_bin = {k: v for k, v in data.items() if k >= n**(power-1) and k < n**power}
        xs = list(my_bin.keys())
        ys = list(my_bin.values())
        pars, cov = curve_fit(f=power_law, xdata=xs, ydata=ys, p0=[0, 0], bounds=(-np.inf, np.inf))
        coefs.append(pars)
        for x in xs:
            fitted_xs.append(x)
            fitted_ys.append(power_law(x, *pars))
        power += 1
    return coefs, fitted_xs, fitted_ys 

# Log binning by mean value
def log_binning(data, n=3):
    data = collections.OrderedDict(sorted(data.items()))
    binned_data = {}
    power = 1
    while n**(power-1) <= max(data.keys()):
        print(n**(power-1), n**power, max(data.keys()))
        my_bin = {k: v for k, v in data.items() if k >= n**(power-1) and k < n**power}
        mean_value = mean(list(my_bin.values()))
        for k, v in my_bin.items():
            binned_data[k] = mean_value
        power += 1
    return binned_data

# %%
def fit_data(data, x_axe, y_axe, fit_func=simple_fit, n=3):
    df = pd.DataFrame(data={x_axe: list(data.keys()), 
                            y_axe: list(data.values())})
    coefs, xs, ys = fit_func(data)
    fitted_df = pd.DataFrame(data={x_axe: xs, 
                                   y_axe: ys})
    return fitted_df, coefs


# %%
def predict_data(xs, coefs, x_axe, y_axe, fit_func=simple_fit, n=3):
    predicted_data = {}
    for x in xs:
        if fit_func == simple_fit:
            a, b = coefs
        elif fit_func == log_fit:
            a, b = coefs[int(log(x, n))]
        predicted_data[x] = power_law(x, a, b)
    predicted_df = pd.DataFrame(data={x_axe: list(predicted_data.keys()), 
                                      y_axe: list(predicted_data.values())})
    return predicted_df


# %%
def plot_data_prediction_fit(training_df, fitted_df, predicted_df, title, x_axe, y_axe, scale='log'):
    g = sns.regplot(x=x_axe, y=y_axe, data=training_df, fit_reg=False, label='data')
    g = sns.regplot(x=x_axe, y=y_axe, data=predicted_df, fit_reg=False, label='predicted data')
    g = sns.lineplot(x=x_axe, y=y_axe, data=fitted_df, label='distribution function')
    g.set_title(title)
    if scale == 'log':
        g.set(xscale='log', yscale='log')

# %%
