import requests
import json
import time

url = 'http://127.0.0.1:8092/query_data_by_page'
# 查询苏州，并进行分页
data = json.dumps({'key_name':'包装','curr_page':'1', "page_size": "4"})
r =requests.post(url, data)
print(r.text)
# 查询 苏州兆鑫驰智能科技有限公
# data = json.dumps({'key_name':'苏州兆鑫驰智能科技有限公','curr_page':'1', "page_size": "10"})
# r =requests.post(url, data)
# print(r.text)
# 根据上面查询的结果，找到这个条数据的文档id，调用接口增加分词，删除分词
# url = 'http://127.0.0.1:8092/add_analyze_token'
# data = json.dumps({'recordId':'fnUNPXcBpOF4N_9ZQYHg','token':'开炮'})
# r =requests.post(url, data)
# time.sleep(2)
# data = json.dumps({'recordId':'fnUNPXcBpOF4N_9ZQYHg','token':'起飞'})
# r =requests.post(url, data)
# time.sleep(2)
# data = json.dumps({'recordId':'fnUNPXcBpOF4N_9ZQYHg','token':'快开炮啊'})
# r =requests.post(url, data)
# time.sleep(2)
# url = 'http://127.0.0.1:8092/remove_analyze_token'
# data = json.dumps({'recordId':'fnUNPXcBpOF4N_9ZQYHg','token':'快开炮啊'})
# r =requests.post(url, data)
# time.sleep(2)
# # 修改is stop
# url = 'http://127.0.0.1:8092/update_isStop'
# data = json.dumps({'recordId':'dyeyR3cBHCAak-AWZltd','isStop':1})
# r =requests.post(url, data)


# 再次查询 苏州兆鑫驰智能科技有限公，查看修改后的结果。
# time.sleep(3)  # es不会立即更新，需要等待3秒
# url = 'http://127.0.0.1:8092/query_data_by_page'
# data = json.dumps({'key_name':'苏州兆鑫驰智能科技有限公','curr_page':'1', "page_size": "10"})
# r =requests.post(url, data)
# print(r.text)
