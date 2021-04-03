import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import urllib.parse
import re
import csv

URL_ROOT = 'http://mojim.com/'
singer_list =['周杰倫',"蔡依林","林俊傑"]
url='ec2-**-***-***-**.compute-1.amazonaws.com'
client=MongoClient(url,username='******',password='******')
client

def song_to_mongo(song_name,b):
    global n
    
    db = client['NOSQL']
    collection = db['songall']

    dic ={'song_name':song_name, 'singer': singer_list[n], 'song':b}
    collection.insert_one(dic)
    
def bb(a):
    for m in a:
        if '\u4e00' <= m <='\u9fa5':
            return True
    return False
    
def song_request(i):
    j = i.get('href')
    sub_resp = requests.get("https://mojim.com" + j)
    
    soup = BeautifulSoup(sub_resp.text, 'lxml')
    song = soup.find(id='fsZx3')
    
    a=str(song).split("<br/>")
    b=[]
    ind=0
    
    if bb(a):
        for m in a:
            if 'dd' in m:
                continue
            if '更多更詳盡歌詞' in m:
                continue
            if '[' in m:
                continue
            if m == "" and ind == 0:
                if ind == 0:
                    continue
                if b[ind-1] =="":
                    continue
            b.append(m)
            ind=ind+1
        ind=-1
        while b[ind]=='':
            b.pop(ind)
        song_to_mongo(i.get('title').split(' 歌')[0],b)
    else:
        return
                
                
def search_song():
    global n
    singer_name = singer_list[n]+ '.html?t1'
    url = urllib.parse.urljoin(URL_ROOT, singer_name)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    singer_url = soup.li.a.get('href')
    
    url = urllib.parse.urljoin(URL_ROOT, singer_url)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    block = soup.find_all('dd', 'hb2')
    block2 = soup.find_all('dd','hb3')
    for i in block: 
        song_left = i.find_all('span','hc3')
        for j in song_left:
            sl = j.find_all('a')
            for k in sl:
                song_request(k)
                
        song_right = i.find_all('span','hc4')
        for j in song_right:
            sr = j.find_all('a')
            for k in sr:
                song_request(k)
    for i in block2: 
        song_left = i.find_all('span','hc3')
        for j in song_left:
            sl = j.find_all('a')
            for k in sl:
                song_request(k)

        song_right = i.find_all('span','hc4')
        for j in song_right:
            sr = j.find_all('a')
            for k in sr:
                song_request(k)         
print(0)
search_song()
print(1)
