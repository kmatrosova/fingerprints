import csv
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA

data = []
data_bis = []
with open('results/variety_vectors.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for i, row in enumerate(spamreader):
        if i > 0:
            data.append([row[1], int(row[3]), int(row[4]), int(row[5])])
            data_bis.append([int(row[3]), int(row[4]), int(row[5])])
            
df = pd.DataFrame.from_records(data, columns=['user_id', 'nb_lang', 'nb_genres', 'nb_decades'])

sns.scatterplot(data=df, x="nb_lang", y="nb_genres")
plt.savefig('figures/lang_x_genres.png')
plt.close()

sns.scatterplot(data=df, x="nb_lang", y="nb_decades")
plt.savefig('figures/lang_x_decades.png')
plt.close()
            
sns.scatterplot(data=df, x="nb_decades", y="nb_genres")
plt.savefig('figures/decades_x_genres.png')
plt.close()

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(data_bis)
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['pc1', 'pc2'])

sns.scatterplot(data=principalDf, x="pc1", y="pc2")
plt.savefig('figures/count_pca.png')
plt.close()