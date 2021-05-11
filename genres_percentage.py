import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


artists = []
with open('../data/my_favorites/my_artists.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 0:
                artists.append([row[0], row[1]])           
artists_df = pd.DataFrame(artists, columns=['artist_id', 'artist_name'])

genre_artist = []
with open('../data/my_favorites/my_artists_tags.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for i, row in enumerate(spamreader):
            if i > 0:
                genre = 'unknown' if row[1] == '' else row[1]
                genre_artist.append([genre, row[0]])                
genre_artist_df = pd.DataFrame.from_records(genre_artist, columns=['genre', 'artist_id'])

artists_df = pd.merge(artists_df, genre_artist_df, left_on='artist_id', right_on='artist_id')  

songs = []
with open('../data/my_favorites/my_songs.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')                    
        for i, row in enumerate(spamreader):
            if i > 0:     
                songs.append([row[0], row[1], row[2]])           
songs_df = pd.DataFrame(songs, columns=['song_id', 'artist_id', 'song_title'])

df = pd.merge(artists_df, songs_df, on='artist_id', 
                 how='left')    
print(df)

G = nx.Graph()
G.add_node('user')
G.add_nodes_from(df.genre.dropna().unique())
my_edges = [('user', g) for g in df['genre']]
G.add_edges_from(my_edges)
G.add_nodes_from(df.artist_name.dropna().unique())
my_edges = [(x, y) for x, y in zip(df['genre'], df['artist_name'])]
G.add_edges_from(my_edges)

#nx.draw(G, with_labels=True)
#plt.savefig("filename.png")

nx.write_gexf(G, "my_favs.gexf")