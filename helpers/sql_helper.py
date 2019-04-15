# -*- coding:utf-8 -*-
import os
import pymssql, pymysql, sqlite3

class MSSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise NameError("Not set database info")
        self.conn = pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise NameError("Connection failed.")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def ExecManyQuery(self, sql, data_list):
        cur = self.__GetConnect()
        import datetime
        end_time_format = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.executemany(sql, data_list)
        self.conn.commit()
        self.conn.close()
        
class MYSQL:
    def __init__(self,host,user,pwd,db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise NameError("Not set database info")
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise NameError("Connection failed.")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def ExecManyQuery(self, sql, data_list):
        cur = self.__GetConnect()
        cur.executemany(sql, data_list)
        self.conn.commit()
        self.conn.close()
        
class Sqlite3:
    def __init__(self, db_path):
        self.db_path = db_path

    def __GetConnect(self):        
        self.conn = sqlite3.connect(self.db_path)     
        if os.path.exists(self.db_path) and os.path.isfile(self.db_path):
            print('硬盘上面:[{}]'.format(self.db_path))   
        else:
            conn = None
            print('内存上面:[:memory:]')
            self.conn = sqlite3.connect(':memory:')
        cur = self.conn.cursor()
        if not cur:
            raise NameError("Connection failed.")
        else:
            return cur

    def ExecQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

    def ExecManyQuery(self, sql, data_list):
        cur = self.__GetConnect()
        cur.executemany(sql, data_list)
        self.conn.commit()
        self.conn.close()