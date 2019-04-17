from itertools import islice
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans 
from sklearn.metrics import silhouette_score
from wordcloud import WordCloud
from github import Github
from pypinyin import lazy_pinyin
import matplotlib.pyplot as plt
import csv
import re

vectorizer = TfidfVectorizer(max_df=0.5, min_df=2, stop_words='english')

def preprocessing(string, lowercase=True):
    '''
    adopted from https://github.com/yoonkim/CNN_sentence/blob/master/process_data.py
    '''
    # preserve English, digital, some punctuations and whitespace characters
    string = re.sub('[^A-Za-z0-9(),.:;!?\-\'&]', ' ', string)
    string = re.sub('\'s', ' \'s', string)
    string = re.sub('\'m', ' \'m', string)
    string = re.sub('\'ve', ' \'ve', string)
    string = re.sub('n\'t', ' n\'t', string)
    string = re.sub('\'re', ' \'re', string)
    string = re.sub('\'d', ' \'d', string)
    string = re.sub('\'ll', ' \'ll', string)
    string = re.sub('\(', ' ( ', string)
    string = re.sub('\)', ' ) ', string)
    string = re.sub(',+', ' , ', string)
    string = re.sub(':+', ' , ', string)
    string = re.sub('\.+', ' . ', string)
    string = re.sub(';+', ' . ', string)
    string = re.sub('!+', ' ! ', string)
    string = re.sub('\?+', ' ? ', string)
    # replace consecutive spaces by one space and remove whitespaces in the front and the end of the text
    string = re.sub(' +', ' ', string).strip()

    if lowercase:
        # convert the text into lower case
        return string.lower()
    return string

def getBioData():
    csvFile = csv.reader(open("following_pagerank.csv",encoding='utf-8',errors='ignore'))
    user_list = [row[1] for row in islice(csvFile,1,None)]
    bio_list = []
    GIT = Github("81bb10423c837b5a6d517b25117a7a95a7ec444a")
    #Group 1
    for userid in user_list[0:199]:
        try:
            print(userid)
            user = GIT.get_user(userid)
            if(user.bio!=None):
                bio = preprocessing(user.bio)
                bio_list.append(bio)
        except:
            print("error")
    #Group 2
    for userid in user_list[200:399]:
        try:
            print(userid)
            user = GIT.get_user(userid)
            if(user.bio!=None):
                bio = preprocessing(user.bio)
                bio_list.append(bio)   
        except:
            print("error")
    print("bio list: ")
    print(bio_list)
    return bio_list

def calTfIdf():
    bio_list = getBioData()
    X = vectorizer.fit_transform(bio_list)
    print('tf-idf:')
    print(X)
    
    return X
    
def kmeansClustering():
    X = calTfIdf()
    silhouette_limit = -1
    for k in range(20,31):
        km = KMeans(n_clusters=k, max_iter=100) 
        kmc = km.fit_predict(X)
        silhouette_coefficient = silhouette_score(X, kmc)
        print('number: %d, silhouette coefficient: %.9f' %(k,silhouette_coefficient))
        if(silhouette_coefficient > silhouette_limit):
            best_k = k
            silhouette_limit = silhouette_coefficient
            best_km = km
    print('The best clustering result is %d' % best_k)
    return best_km,best_k

def wordCloud():
    best_km,best_k = kmeansClustering()
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

wordCloud()