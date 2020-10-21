# -*- coding:utf-8 -*-
import json
import redis

# 缓存过期时间 单位是秒！
CACHE_TIME_OUT = 150

# sql数据库的连接实例
# redis的链接实例
redisdb = redis.Redis(host='127.0.0.1', decode_responses=True)

def GetInfo(data):
    data=json.dumps(data,ensure_ascii=False)
    print(type(data))
    list = redisdb.get(data)
    return list



def Redis_save(k,v):
    k = json.dumps(k, ensure_ascii=False)
    v = json.dumps(v,ensure_ascii=False)
    redisdb.setex(k, CACHE_TIME_OUT, v)
