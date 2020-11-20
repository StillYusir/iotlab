# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

from flask_restful import abort
import json

import MySQLdb
import configparser
from datetime import datetime
import time


class SchemaMysql:
    # 初始化用户数据 isdrop参数为是否删除目标库多余的字段
    def __init__(self, src_info, des_info, isdrop):
        self.src_ip = src_info[0]
        self.src_db_user = src_info[1]
        self.src_db_pass = src_info[2]
        self.des_ip = des_info[0]
        self.des_db_user = des_info[1]
        self.des_db_pass = des_info[2]
        self.isDrop = isdrop

    # 初始化不同的数据库
    def init(self, src_db, des_db):
        self.dbsrc = self.connect_db(self.src_ip, src_db, self.src_db_user, self.src_db_pass)
        self.dbdes = self.connect_db(self.des_ip, des_db, self.des_db_user, self.des_db_pass)
        self.cursorsrc = self.dbsrc.cursor()
        self.cursordes = self.dbdes.cursor()

    # 手动关闭数据库
    def close_db(self):
        self.cursorsrc.close()
        self.cursordes.close()
        self.dbsrc.close()
        self.dbdes.close()

    # 连接数据库
    def connect_db(self, ip, db, db_user, db_pass):
        db = MySQLdb.connect(ip, db_user, db_pass, db)
        return db

    # 获取数据库中的表
    def getTable(self, cursor):
        cursor.execute("show tables")
        tablelist = []
        for tb in cursor.fetchall():
            tablelist.append(tb[0])
        return tablelist

    # 获取创表语句
    def getField(self, cursor, tb):
        sql = "show create table " + str(tb)
        cursor.execute(sql)
        return cursor.fetchone()

    # 生成需要执行的sql语句
    def createSql(self, tb, mode, F):
        if mode == 'c':
            sql = "alter table " + str(tb) + " change " + F[0] + " " + F[0]
        elif mode == 'a':
            sql = "alter table " + str(tb) + " add " + F[0]
        elif mode == 'd':
            sql = "alter table " + str(tb) + " drop column " + F[0]
            return sql
        else:
            return None
        for d in range(1, len(F)):
            sql = sql + " " + F[d]
        return sql

    # 检测两个数据表字段是否一样
    def checkField(self, tb, sqlSrc, sqlDes):
        runList = []
        srcList = sqlSrc[1].replace(",", "").split("\n")[1:-1]  # 去除不需要的数据
        desList = sqlDes[1].replace(",", "").split("\n")[1:-1]
        for i in srcList:
            srcF = i.split()
            for j in desList:
                desF = j.split()
                if srcF[0] == desF[0]:
                    if len(srcF) == len(desF):
                        for c in range(1, len(srcF)):
                            if srcF[c] != desF[c]:
                                runList.append(self.createSql(tb, "c", srcF))
                    else:
                        runList.append(self.createSql(tb, "c", srcF))
                    break;
            else:
                runList.append(self.createSql(tb, "a", srcF))
        if self.isDrop:
            srcList = [x.split()[0] for x in srcList]
            desList = [x.split()[0] for x in desList]
            for desI in desList:
                if desI not in srcList:
                    runList.append(self.createSql(tb, "d", [desI]))
        return runList

    # 执行 删除字段 增加字段 修改字段的sql语句
    def runExec(self, runlist):
        for run in runlist:
            print("run")
            self.cursordes.execute(run)

    # 检测数据表是否一样如果没有则在目标主机上创建
    def checkTable(self, tbSrc, tbDes, cursrc, curdes):
        for tbA in tbSrc:
            dataSrc = self.getField(cursrc, tbA)
            if tbA in tbDes:
                runlist = self.checkField(tbA, dataSrc, self.getField(curdes, tbA))
                if not runlist is None:
                    self.runExec(runlist)
            else:
                curdes.execute(dataSrc[1].replace("\n", ""))

    # 开始运行
    def run(self):
        print("Run")
        srctable = self.getTable(self.cursorsrc)
        destable = self.getTable(self.cursordes)
        self.checkTable(srctable, destable, self.cursorsrc, self.cursordes)


"""
获取config文件信息
包括  ip  用户  密码   表
"""


def getConfDBList():
    src_list = []
    des_list = []
    config = configparser.ConfigParser()
    config.read("config.cfg")
    src_list.append(config.get('SRC', 'ip'))
    src_list.append(config.get('SRC', 'user'))
    src_list.append(config.get("SRC", 'pass'))
    src_list.append(config.get("SRC", 'db'))

    des_list.append(config.get('DES', 'ip'))
    des_list.append(config.get('DES', 'user'))
    des_list.append(config.get("DES", 'pass'))
    des_list.append(config.get("DES", 'db'))
    return [src_list, des_list]


def readAndWrite():
    # db = pymysql.connect('127.0.0.1', 'root', 'yeya0422', 'recruitment', 3306, charset='utf8')
    write = pymysql.connect('127.0.0.1', 'root', 'yeya0422', 'yeya', 3306, charset='utf8')
    Wcursor = write.cursor()
    writeSql_res = "insert into yeya.res select * from kunshan_db.res"    writeSql_job = "insert into yeya.pos select * from kunshan_db.pos"
    try:
        Wcursor.execute(writeSql_res)
        Wcursor.execute(writeSql_job)
        write.commit()
    except:
        write.rollback()
        write.close()
    # db.close()


def clear():
    db = pymysql.connect('127.0.0.1', 'root', 'yeya0422', 'yeya', 3306, charset='utf8')
    cursor = db.cursor()
    sql_res = "DROP table res"
    sql_job = "DROP table pos"
    cursor.execute(sql_res)
    cursor.execute(sql_job)
    db.close()


def Update_Set(id, action):
    # 打开数据库链接
    write = pymysql.connect('127.0.0.1', 'root', 'yeya0422', 'yeya', 3306, charset='utf8')
    Wcursor = write.cursor()
    sql_del = "delete from yeya.pos WHERE JobID = %s" % (id)
    Sql_ins = "insert into yeya.pos select * from kunshan_db.pos WHERE JobID = %s" % (id)
    try:
        if action == "update":
            Wcursor.execute(sql_del)
            Wcursor.execute(Sql_ins)
        if action == "delete":
            Wcursor.execute(sql_del)
        if action == "insert":
            Wcursor.execute(Sql_ins)
        write.commit()
    except:
        write.rollback()
        write.close()


def maskrcnn():
    try:
        if not request:
            abort(400)
        data = json.loads(request.data.decode('utf-8'))
        print(data)
        for key in data:
            jobID = key['jobID']
            action = key['action']
            Update_Set(jobID, action)

        return jsonify({'code': 1, 'message': 'success'})
    except Exception as e:
        return jsonify({'code': 0, 'message': str(e)})


@app.route('/structure')
def mainfun():
    # clear()
    flag = True
    while True:

        # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        # 结构同步
        list = getConfDBList()
        src_info = ['127.0.0.1', 'root', 'yeya0422']
        des_info = ['127.0.0.1', 'root', 'yeya0422']
        src_db = list[0][3].split(",")
        des_db = list[1][3].split(",")
        print("Begin")
        schema = SchemaMysql(src_info, des_info, True)
        for i in range(len(src_db)):
            if src_db[i] and des_db[i]:
                schema.init(src_db[i], des_db[i])
                schema.run()
                schema.close_db()
        # 数据同步
        if flag:
            readAndWrite()
            flag = False
        print("success")

        time.sleep(30)


@app.route('/')
def hello_world():
    # 增量同步
    str = maskrcnn()
    return str


if __name__ == '__main__':
    app.run()
