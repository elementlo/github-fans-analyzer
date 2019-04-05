# -*- coding: utf-8 -*-
from github import Github, StatsCommitActivity
from multiprocessing import Pool, cpu_count, Lock
import pandas as pd

# or using an access token
GIT = Github("81bb10423c837b5a6d517b25117a7a95a7ec444a")

# LOCK = threading.Lock()     # 全局资源锁
lock = Lock()

PD_FORMAT = {
    "created_at" : [],
    "login" : [],
    "name" : [],
    "type" : [],
    "company" : [],
    "location" : [],
    "contributions" : [],
    "public_repos" : [],
    "followers" : [],
    "following" : [],
    "bio":[],
    "blog":[],
    "repositories":[]
}

def _task(NamedUser):
    """多线程任务执行
    Arguments:
        NamedUser {[class]} -- [github.NamedUser.NamedUser]
    """
    
    created_at = NamedUser.created_at.year
    login = NamedUser.login
    name = NamedUser.name
    utype = NamedUser.type
    company = NamedUser.company
    location = NamedUser.location
    contributions = NamedUser.contributions
    public_repos = NamedUser.public_repos
    followers = NamedUser.followers
    following = NamedUser.following
    bio=NamedUser.bio
    blog=NamedUser.blog
    repositories=NamedUser.public_repos
    print('current following: ' + login)
    # lock.acquire()
    PD_FORMAT['created_at'].append(created_at)
    PD_FORMAT['login'].append(login)
    PD_FORMAT['name'].append(name)
    PD_FORMAT['type'].append(utype)
    PD_FORMAT['company'].append(company)
    PD_FORMAT['location'].append(location)
    PD_FORMAT['contributions'].append(contributions)
    PD_FORMAT['public_repos'].append(public_repos)
    PD_FORMAT['followers'].append(followers)
    PD_FORMAT['following'].append(following)
    PD_FORMAT['bio'].append(bio)
    PD_FORMAT['blog'].append(blog)
    PD_FORMAT['repositories'].append(repositories)
    # print(PD_FORMAT)
    # lock.release()
    

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
    print('contributions:'+ str(NamedUser.contributions))
    print('followings :' + str(NamedUser.following))
    print('followings_url:' + NamedUser.following_url)
    print('repositories:' + str(NamedUser.public_repos))
    print('--------------------------------')

def get_all_followings(user_name):
    """[get all followers] 
    Arguments:
        user_name {[string]} -- [user to analysis]
    """
    center_user = GIT.get_user(user_name)
    _print_user_profile(center_user)
    for follower in center_user.get_following():
        _task(follower)

    df = pd.DataFrame(PD_FORMAT)
    df.to_csv('followings.csv')
    print('-----end-----')

def main():
    get_all_followings('wangshub')

if __name__ == '__main__':
    main()