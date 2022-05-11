# coding:utf-8

import tweepy
import multiprocessing as mp
import warnings
import time
import socket
import pandas as pd
import random
import os
from concurrent import futures

warnings.filterwarnings(action = 'ignore')
# download('punkt')

# 我的推特专属API入口

class WebScratch():
    def __init__(self):
        self.API_key = 'keQ8wGpnz2XP24WfiUcvI9ADg'
        self.API_key_secret = 'zmrJWddMWACpzIH1U3AtVV3TGsKnFdbl8E2JgyQTYWCBwwT3Ec'
        self.token = 'AAAAAAAAAAAAAAAAAAAAAINKWQEAAAAABC7MrWgUIryCivmuFjKaIfYzAcw%3DEwZiW2KGRxiO9nvkzJjvmNVTqU64eiArNDUmFn5Y2dBMYYcEcB'
        self.APP_ID = '22628995'
        self.access_token = '1465439601762443279-AyV3JzAKSyR8QYNfy8ki0GQDb0hNm1'
        self.access_token_secret = 'c5uCOvwxHW7VmD5UGId82IxWNYt4qkg1PVGQyDgbHDikS'
        self.proxy = socket.gethostbyname(socket.gethostname())

    def connect(self):
        try:
            auth = tweepy.OAuthHandler(self.API_key, self.API_key_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)
            return tweepy.API(auth, wait_on_rate_limit=True)
        except Exception as e:
            print("unsuccessful connect", e)
            exit()

class DataProcess(WebScratch):

    def getContent(self, name, nums):
        # time.sleep(100)
        api = WebScratch().connect()
        content = tweepy.Cursor(api.search_tweets, name, lang = "en", tweet_mode="extended").items(nums)
        return list(map(lambda x:
        str(x._json['id_str']) + " - " + str(x._json['created_at']) + " - " + str(x._json['full_text']) + " - " +
        str(x._json['retweet_count']) + " - " + str(x._json['favorite_count']) + " - " + str(x._json['in_reply_to_status_id_str'])
        + " - " +str(x._json['in_reply_to_user_id_str']) + " - " + str(x._json['entities']['user_mentions']) + " - " + str(x._json['user']['id_str'])
        + " - " + str(x._json['user']['screen_name']) + " - " + str(x._json['user']['location']) +" - " +
        str(x._json['user']['url']) + " - "+ str(x._json['user']['followers_count']) +" - " + str(x._json['user']['favourites_count']), content))

        # return list(map(lambda x: x._json['created_at']+" - "+x._json['full_text'], content))

    def toDf(self, name, nums):
        ls = list(set(self.getContent(name, nums)))
        # ls = self.getContent(name, nums)
        df = pd.DataFrame(list(map(lambda x: x.split(" - "), ls)))
        # try:
            # df.columns = ['id','created_at','full_text','retweet_count','favorite_count','in_reply_to_status_id','in_reply_to_user_id',
     # 'user_mention','user_id','user.screen_name','user.location','user.url','user.followers_count','user.favourites_count']
     #        return df
     #    except:
        return df

    def toExcel(self, name, nums, path):
        # try:
        self.toDf(name, nums).to_excel(path, header = True)
        print("PID = {}, ParentPID = {}".format(os.getpid(), os.getppid()))
        return ("successful write in")

pro = DataProcess()


# 参数
name = "from:Shell"   # shell发出的，少可以不要
name2 = "@Shell"  # 点名shell的
name3 = "to:Shell"  # 发给Shell的
name4 = '"Shell"'  # 包含Shell的
name5 = "Shell" # 包含Shell的
ls = [name, name2, name3, name4, name5]
nums = 5000
path = []
for i in range(0, len(ls)):
    path.append( "D:\\上课资料库\\social media and web analysis\\结课论文\\dataset_%d.xlsx"%(i+1))
#     print(pro.toExcel(ls[i], nums, path))
#     time.sleep(10)
# # print(pro.toDf(name, nums)['full_text'])


def manul_execute(ls, path):
    print("进程开始")
    # 自行创建进程池
    process_pool = [
        mp.Process(target=pro.toExcel, args=(ls[0], nums, path[0])),
        mp.Process(target=pro.toExcel, args=(ls[1], nums, path[1])),
        mp.Process(target=pro.toExcel, args=(ls[2], nums, path[2])),
        mp.Process(target=pro.toExcel, args=(ls[3], nums, path[3])),
        mp.Process(target=pro.toExcel, args=(ls[4], nums, path[4]))
    ]
    for p in process_pool:
        p.start()  # 进程开始
        time.sleep(80)
    for p in process_pool:
        p.join()   # 进程阻塞





if __name__ == "__main__":
    # execute_by_future()
    manul_execute(ls, path)
