from locust import HttpUser,between,task
import json
import random

class ScriptTasks(HttpUser):
    wait_time = between(1,2)
    def read_data(self):
        job_index = []
        job_body = []
        job_flag = 0
        res_index = []
        res_body = []
        res_flag = 0
        with open(r"D:\Pycharm\workspace\PycharmProjects\recommendation_system\SearchModule\press_test\职位样本数据（少量）.csv", "r") as f:
            for line in f.readlines():
                if job_flag == 0:
                    line = line.split('\n')
                    line = line[0].split(',')
                    for item in line:
                        job_index.append(item)
                    job_flag += 1
                else:
                    line = line.split('\n')
                    line = line[0].split(',')
                    tmp = []
                    for item in line:
                        tmp.append(item)
                    job_body.append(tmp)
                    job_flag += 1
        with open(r"D:\Pycharm\workspace\PycharmProjects\recommendation_system\SearchModule\press_test\简历样本数据（少量）.csv", "r") as f:
            for line in f.readlines():
                if res_flag == 0:
                    line = line.split('\n')
                    line = line[0].split(',')
                    for item in line:
                        res_index.append(item)
                    res_flag += 1
                else:
                    line = line.split('\n')
                    line = line[0].split(',')
                    tmp = []
                    for item in line:
                        tmp.append(item)
                    res_body.append(tmp)
                    res_flag += 1
        return job_index, job_body, res_index, res_body

    def random_read(self,job_index, job_body, res_index, res_body):
        random_flag = random.randint(1, 10)
        random_job = []
        random_res = []
        job_request = {}
        res_request = {}
        for i in range(random_flag):
            tmp0 = random.randint(0, 30)
            tmp1 = random.randint(0, 25)
            if tmp0 not in random_job:
                random_job.append(tmp0)
            if tmp1 not in random_res:
                random_res.append(tmp1)
        # print(random_job,random_res)
        for item in random_job:
            job_request[job_index[item]] = job_body[random.randint(0, 81)][item]
        for item in random_res:
            res_request[res_index[item]] = res_body[random.randint(0, 141)][item]
        res_request = json.dumps(res_request, ensure_ascii=False)
        job_request = json.dumps(job_request, ensure_ascii=False)
        return res_request,job_request

    @task(1)
    def test_job_search(self):
        job_index, job_body, res_index, res_body = self.read_data()
        res_request, job_request = self.random_read(job_index, job_body, res_index, res_body)
        job_request=json.loads(job_request,encoding='utf-8')

        res=self.client.post("/api/pos-result", json=job_request)

        if res.status_code==200:
            print("success","request:",job_request,"resoponse:",res)
        else:
            print("fail",job_request)

    @task(1)
    def test_res_search(self):
        job_index, job_body, res_index, res_body = self.read_data()
        res_request, job_request = self.random_read(job_index, job_body, res_index, res_body)
        res_request=json.loads(res_request,encoding="utf-8")

        res=self.client.post("/api/resume_result", json=res_request)

        if res.status_code==200:
            print("success","request:",res_request,"resoponse:",res)
        else:
            print("fail",res_request)


    # @task(2)
    # def test_index(self):
    #     header={"Content-Type": "application/josn;charset=utf-8"}
    #     req=self.client.get("/",verify=False)