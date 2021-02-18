# %%


# %%
big_likes, big_users, big_items, big_user_items, big_item_users = get_data_from_csv('../data/users_bipartite_aligned_artist_1000000.csv')
print('\nNumber or users:', len(big_users))
print('\nNumber or artists:', len(big_items))

# %%
G = Graph()
# Add nodes with the node attribute "bipartite"
G.add_nodes_from(big_users, bipartite=0)
G.add_nodes_from(big_items, bipartite=1)
# Add edges only between nodes of opposite node sets
G.add_weighted_edges_from(big_likes)

# %%
print('nb of components', sum(1 for x in connected_components(G)))

# %%
data_comp = pd.DataFrame(data={'size': list(nb_comp_per_size.keys()), 
                               'nb_components': list(nb_comp_per_size.values())})
g = sns.regplot(x='size', y='nb_components', data=data_comp, fit_reg=False)
g.set(xscale="log", yscale="log")
g.set_title('Distibution of number of components by size')