import csv
from itertools import islice
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans 
from sklearn.metrics import silhouette_score
from wordcloud import WordCloud
import matplotlib.pyplot as plt


csvFile = csv.reader(open("followings.csv",encoding='utf-8',errors='ignore'))

bio_list = [row[11] for row in islice(csvFile,1,None)]

print(bio_list)

vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english') 
X = vectorizer.fit_transform(bio_list)
print('tf-idf:')
print(X)

print('====================Perform k-means clustering and Compute the silhouette coefficient======================')
silhouette_limit = -1
for k in range(4,7):
    km = KMeans(n_clusters=k, max_iter=100) 
    kmc = km.fit_predict(X)
    silhouette_coefficient = silhouette_score(X, kmc)
    print('number: %d, silhouette coefficient: %.9f' %(k,silhouette_coefficient))
    if(silhouette_coefficient > silhouette_limit):
        best_k = k
        silhouette_limit = silhouette_coefficient
        best_km = km
print('The best clustering result is %d' % best_k)

print('====================Compute the wordcloud======================')
order_centroids = best_km.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
cluster_item=''
for i in range(best_k):
    print('Cluster %d:' % i, end='')
    for ind in order_centroids[i, :10]:
        print(' %s' % terms[ind], end='')
        cluster_item=cluster_item+' '+terms[ind]
    print()
    wordcloud = WordCloud().generate(cluster_item)
    wordcloud.to_file('wordcloud%d'%i+'.png')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    cluster_item=''