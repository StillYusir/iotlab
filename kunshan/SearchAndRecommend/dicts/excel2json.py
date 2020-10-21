import xlrd
import json

def ProduceCarererDict():
    jsontext = {"career_categories":[]}
    data = xlrd.open_workbook("新人才网数据字典.xlsx")
    print(str(data.sheet_names()))
    table = data.sheet_by_name('职位类别(全部)')
    for row in range(1,table.nrows):
        row_val = table.row_values(row)
        jsontext["career_categories"].append({str(row_val[2]):row_val[1]})
    #print(jsontext)
    jsondata = json.dumps(jsontext,indent=4,separators=(",",":"),ensure_ascii=False)
    print(jsondata)
    f=open("career.json","w")
    f.write(jsondata)
    f.close()



#生成职位类别为大类的字典
def ProduceJobDict():
    jsontext = {"job_categories":{}}
    data = xlrd.open_workbook("新人才网数据字典.xlsx")
    print(str(data.sheet_names()))
    table = data.sheet_by_name('职位类别(大类)')
    for row in range(1,table.nrows):
        row_val = table.row_values(row)
        jsontext["job_categories"][str(row_val[2])]=row_val[1]
    #print(jsontext)
    jsondata = json.dumps(jsontext,indent=4,separators=(",",":"),ensure_ascii=False)
    print(jsondata)
    f=open("job.json","w")
    f.write(jsondata)
    f.close()







if __name__=="__main__":
    print("start preprocess data")
    ProduceJobDict()