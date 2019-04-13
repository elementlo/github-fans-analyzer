from itertools import islice
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans 
from sklearn.metrics import silhouette_score
from wordcloud import WordCloud
from github import Github
from pypinyin import lazy_pinyin
import matplotlib.pyplot as plt
import csv



csvFile = csv.reader(open("following_pagerank.csv",encoding='utf-8',errors='ignore'))

user_list = [row[1] for row in islice(csvFile,1,None)]

bio_list = []

GIT = Github("81bb10423c837b5a6d517b25117a7a95a7ec444a")

#优秀用户
for userid in user_list[0:199]:
    user = GIT.get_user(userid)
    if(user.bio!=None):
        bio_list.append(user.bio)

#需要被推荐的用户
for userid in user_list[848:]:
    user = GIT.get_user(userid)
    if(user.bio!=None):
        bio_list.append(user.bio)

print(bio_list)

print('====================TF-IDF======================')
vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english') 
X = vectorizer.fit_transform(bio_list)
print('tf-idf:')
print(X)

print('====================Perform k-means clustering and Compute the silhouette coefficient======================')
silhouette_limit = -1
for k in range(30,33):
    km = KMeans(n_clusters=k, max_iter=100) 
    kmc = km.fit_predict(X)
    silhouette_coefficient = silhouette_score(X, kmc)
    print('number: %d, silhouette coefficient: %.9f' %(k,silhouette_coefficient))
    if(silhouette_coefficient > silhouette_limit):
        best_k = k
        silhouette_limit = silhouette_coefficient
        best_km = km
print('The best clustering result is %d' % best_k)

print('====================Wordcloud======================')
order_centroids = best_km.cluster_centers_.argsort()[:, ::-1]
terms = lazy_pinyin(vectorizer.get_feature_names())
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