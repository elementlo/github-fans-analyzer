# -*- coding: utf-8 -*-
from github import Github, StatsCommitActivity
from multiprocessing import Pool, cpu_count, Lock
import pandas as pd
import csv
import networkx as nx

# or using an access token
GIT = Github("81bb10423c837b5a6d517b25117a7a95a7ec444a")

list_all_following=[]
column_name=['User','Following']

def _task(list_following,i):
    """
    Arguments:
        NamedUser {[class]} -- [github.NamedUser.NamedUser]
    """
    i += 1
    print(i)
    if i==2:
        return
    for following in list_following:
        login = following.login
        list_following_fo = following.get_following()
        for following_fo in list_following_fo:
            list_user=[]
            list_user.append(login)
            list_user.append(following_fo.login)
            list_all_following.append(list_user)
        print(list_all_following)
    _task(list_following_fo,i)


def _print_user_profile(NamedUser):
    """[print user profile]  
    Arguments:
        user {[class]} -- [github.NamedUser.NamedUser]
    """
    print('--------------------------------')
    print(NamedUser.created_at.year)
    print('login     :' + NamedUser.login)
    print('name      :' + NamedUser.name)
    print('type      :' + NamedUser.type)
    print('company   :' + NamedUser.company)
    print('location  :' + NamedUser.location)
    print('contributions:' + str(NamedUser.contributions))
    print('followers :' + str(NamedUser.followers))
    print('followers_url:' + NamedUser.followers_url)
    print('--------------------------------')


def get_all_followings(user_name):
    """[get all followers] 
    Arguments:
        user_name {[string]} -- [user to analysis]
    """
    center_user = GIT.get_user(user_name)
    _print_user_profile(center_user)
    login = center_user.login
    list_following = center_user.get_following()
    for following in list_following:
        list_user=[]
        list_user.append(login)
        list_user.append(following.login)
        list_all_following.append(list_user)
    print(list_all_following)
    i=0
    _task(list_following,i)
    df = pd.DataFrame(data=list_all_following,columns = column_name)
    df.to_csv('following_pagerank.csv')
    print('-----end-----')

def main():
    get_all_followings('wangshub')


if __name__ == '__main__':
    main()
