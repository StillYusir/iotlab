from locust import HttpUser,between,task,TaskSet
import random
import os
import json

class WebsiteUser(HttpUser):

    wait_time = between(1,2)
    host = "http://0.0.0.0:8881"

    @task(1)
    def test_pos(self):
        post_url = '/search/pos-result'
        pos_request = {
            "pageIndex": "3",
            "pageSize": "10",
            "keyword": "java工程师",
            "jobType": "",
            "jobArea": "32058300",
            "salary": "",
            "salaryLabel": "5-8k",
            "workExp": "3504",
            "edu": "3404",
            "comTrade": "",
            "comScale": "1303",
            "perID": ""
        }
        pos_request = json.dumps(pos_request)
        response = self.client.post(post_url, data=pos_request)

        if response.status_code != 200:
            print("返回异常")
            print("请求返回状态码:", response.status_code)
        elif response.status_code == 200:
            print("返回正常")

if __name__ == '__main__':
    os.system('locust -f test.py --web-host="0.0.0.0"')
