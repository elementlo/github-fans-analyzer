# -*- coding: utf-8 -*-
from multiprocessing import Pool, cpu_count, Lock, Manager
from fake_useragent import UserAgent
import random
import pandas as pd
import threading
import csv
import requests
from bs4 import BeautifulSoup
import ssl
try:
    from functools import namedtuple
except ImportError:
    from collections import namedtuple
ssl._create_default_https_context = ssl._create_unverified_context

ua = UserAgent()
# HEADER = {'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}
HEADER = {'User-Agent': ua.random}

COLUMNS = ['user','name','position','repositories','stars', 'followers', 'following', 'contributions']
PROFILE = namedtuple('PROFILE', COLUMNS)
Result = Manager().list()

DF = pd.DataFrame(columns=COLUMNS, index=["0"])
CSV_FILE = 'followers.csv'
lock = threading.Lock()     #lock


def _str_2_int(stri):
    if 'k' in stri:
        return int(float(stri[:-1]) * 1000)
    if ',' in stri:
        return int(stri.replace(',', ''))
    else:
        return int(stri)

def user_crawler(user):
    """crawl user profile
    
    Arguments:
        url {string} -- [description]
    """
    url = 'https://github.com/{}'.format(user)
    values = [None] * len(COLUMNS)
    values[COLUMNS.index('user')] = user
    try:
        html = requests.get(url, headers=HEADER, timeout=(5,10)).text
        soup = BeautifulSoup(html, 'lxml')
        
        tag_name = soup.find_all('span', class_='p-name vcard-fullname d-block')
        if len(tag_name) > 0:
            name = tag_name[0].text
            if len(name) > 0:
                values[COLUMNS.index('name')] = name

        tag_position = soup.find_all('span', class_='p-label')
        if len(tag_position) > 0:    
            position = tag_position[0].text
            values[COLUMNS.index('position')] = position

        tags_overview = soup.find_all('span', class_='Counter')
        repositories = _str_2_int(tags_overview[0].text.replace('\n', '').replace(' ', ''))
        stars =        _str_2_int(tags_overview[1].text.replace('\n', '').replace(' ', ''))
        followers =    _str_2_int(tags_overview[2].text.replace('\n', '').replace(' ', ''))
        following =    _str_2_int(tags_overview[3].text.replace('\n', '').replace(' ', ''))
        values[COLUMNS.index('repositories')] = repositories
        values[COLUMNS.index('stars')] = stars
        values[COLUMNS.index('followers')] = followers
        values[COLUMNS.index('following')] = following
        
        tag_contributions = soup.find_all('h2', class_='f4 text-normal mb-2')
        try:
            contributions = _str_2_int(tag_contributions[0].text.replace('\n', '').replace(' ', '').replace('contributionsinthelastyear', ''))
        except Exception as err:
            contributions = _str_2_int(tag_contributions[0].text.replace('\n', '').replace(' ', '').replace('contributioninthelastyear', ''))
        values[COLUMNS.index('contributions')] = contributions
        with lock:
            print(values)
            Result.append(values)
    except Exception as e:
        print(e)

def get_all_followers(user):
    """get all followers of user
    
    Arguments:
        user {string} -- [description]
    """
    followers_list = []
    idx = 0
    url = 'https://github.com/{}?page={}&tab=followers'
    while True:
        idx += 1
        page_url = url.format(user, idx) 
        try:
            print(page_url)
            html = requests.get(page_url, headers=HEADER, timeout=(4,5)).text
            soup = BeautifulSoup(html, 'lxml')
            tag_names = soup.find_all('span', class_='link-gray pl-1')

            for name in tag_names:
                followers_list.append(name.text)
            
            if 'Next' in html:
                next_button=soup.find('button', {'class':'btn btn-outline BtnGroup-item'}).string
                print(next_button)
                if next_button == 'Next':
                    print(len(followers_list))
                    break
            else:
                break
        except Exception as e:
            print(e)
    return followers_list
                
def save():
    """ 将数据保存至本地
    """
    with open("data/result.csv", "w+") as f:
        global Result
        f_csv = csv.writer(f)
        f_csv.writerow(COLUMNS)
        f_csv.writerows(Result)
        print('data saved')

followers_list = []

def main():
    """main process
    """
    main_user = 'Dorvaryn'
    print('Crawling followers lists, wait a moment ...')
    followers_list = get_all_followers(main_user)
    pool = Pool(processes=cpu_count())
    
    for user in followers_list:
        pool.apply_async(user_crawler, args=(user, ))

    pool.close()
    pool.join()
    save()

if __name__ == '__main__':
    main()