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
