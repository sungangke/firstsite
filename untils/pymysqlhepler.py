import pymysql

def get_list(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
    course = conn.cursor(cursor=pymysql.cursors.DictCursor)
    course.execute(sql,args)
    result = course.fetchall()
    course.close()
    conn.close()
    return result

def get_one(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
    course = conn.cursor(cursor=pymysql.cursors.DictCursor)
    course.execute(sql,args)
    result = course.fetchone()
    course.close()
    conn.close()
    return result

def movde_list(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
    course = conn.cursor(cursor=pymysql.cursors.DictCursor)
    course.execute(sql,args)
    conn.commit()
    course.close()
    conn.close()

def create(sql,args):
    conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
    course = conn.cursor(cursor=pymysql.cursors.DictCursor)
    course.execute(sql, args)
    conn.commit()
    last_word = course.lastrowid
    course.close()
    conn.close()
    return last_word


class SqlHelper(object):

    def __init__(self):
        #这里可以读取配置文件的方式，把链接的密码端口
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
        self.course = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self,sql,args):
        self.course.execute(sql,args)
        result = self.course.fetchall()
        return result

    def get_one(self,sql,args):
        self.course.execute(sql,args)
        result = self.course.fetchone()
        return result

    def modify(self,sql,args):
        self.course.execute(sql,args)
        self.conn.commit()

    def create(self,sql,args):
         self.course.execute(sql,args)
         self.conn.commit()
         return self.course.lastrowid

    def multiple_modify(self,sql,args):
        self.course.executemany(sql,args)
        self.conn.commit()

    def close(self):
        self.course.close()
        self.conn.close()

