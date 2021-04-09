import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import urllib.parse
import re
from urllib import request
from urllib.parse import quote
import string


URL_ROOT = 'http://mojim.com/'
singer_list =['周杰倫',"蔡依林","林俊傑"]
n = 0
url='ec2-**-***-***-**.compute-1.amazonaws.com'
client=MongoClient(url,username='***',password='admin') #密碼太簡單，被盜了

    
def song_to_mongo(song_name,b):
    global n
    
    db = client['NOSQL']
    collection = db['songall']
    url = "https://www.youtube.com/results?search_query=" + re.sub('[ +]', '', song_name)+singer_list[n]
    try:
        s = quote(url,safe=string.printable)
    except:
        print(song_name)
        print(url+" 失敗")
        return
    response = request.urlopen(s)
    video_ids = re.findall(r"watch\?v=(\S{11})", response.read().decode())
    
    for i in video_ids:
        YoutuberSongUrl="https://www.youtube.com/embed/" + i
        break
    dic ={'song_name':song_name, 'singer': singer_list[n],'YoutuberSongUrl': YoutuberSongUrl, 'song':b}
    collection.insert_one(dic)
    
#處理空list
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
            if m == "":
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
                
                
def search_song(a):
    global n
    singer_name = a+ '.html?t1'
    url = urllib.parse.urljoin(URL_ROOT, singer_name)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    singer_url = soup.li.a.get('href')
    
    url = urllib.parse.urljoin(URL_ROOT, singer_url)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    block = soup.find_all('dd', 'hb2')
    block2 = soup.find_all('dd','hb3')
    song_count=0
    for i in block: 
        song_left = i.find_all('span','hc3')
        for j in song_left:
            sl = j.find_all('a')
            for k in sl:
                song_count=song_count+1
                song_request(k)
        song_right = i.find_all('span','hc4')
        for j in song_right:
            sr = j.find_all('a')
            for k in sr:
                song_count=song_count+1
                song_request(k)
        if song_count>=20:
            break
    for i in block2: 
        song_left = i.find_all('span','hc3')
        for j in song_left:
            sl = j.find_all('a')
            for k in sl:
                song_count=song_count+1
                song_request(k)
        song_right = i.find_all('span','hc4')
        for j in song_right:
            sr = j.find_all('a')
            for k in sr:
                song_count=song_count+1
                song_request(k)
        if song_count>=45:
            break
    n +=1
for a in singer_list:
    print(a)
    search_song(a)
    print(a)
#search_song()
print("結束")
# print(singer_list[n])
