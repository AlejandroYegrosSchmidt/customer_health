import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

dataset = pd.read_csv(r'dataset\dataset_food.csv', low_memory=False)

df = pd.read_csv(r'resultado.csv', low_memory=False)
all_data = df.copy()
df = df.iloc[:,1:].dropna().reset_index()

#corr  = df.corr()


#kmeans = KMeans(n_clusters=3, random_state=42)
#kmeans.fit(df)

#df['cluster'] = kmeans.labels_
def nro_cluster():
    # Método del Codo para determinar el número óptimo de clusters
    inertia = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(df)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), inertia, marker='o')
    plt.xlabel('Número de Clusters')
    plt.ylabel('Inercia')
    plt.title('Método del Codo para Determinar el Número Óptimo de Clusters')
    plt.show()
#sns.pairplot(df.iloc[:,1:], hue='cluster',height=2.5, diag_kind='kde',palette='deep')

