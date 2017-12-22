
import pymysql
from django.shortcuts import render,redirect

def classes(request):
    conn = pymysql.connect(host='localhost',port=3306,user='kk',passwd='123',db='webdb',charset='utf8')
    course=conn.cursor(cursor=pymysql.cursors.DictCursor)
    course.execute("select id,title from class")
    res = course.fetchall()
    course.close()
    conn.close()
    return render(request,'studentmanagent/class_list.html',{'class_list':res})

def add_class(request):
    if request.method == "GET":
        return render(request,'studentmanagent/add_class.html')
    else:
        v = request.POST.get('title')
        conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
        course = conn.cursor(cursor=pymysql.cursors.DictCursor)
        course.execute("insert into class (title) values (%s)",[v,])
        conn.commit()
        course.close()
        conn.close()
        return redirect('/classes/')

def edit_class(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
        course = conn.cursor(cursor=pymysql.cursors.DictCursor)
        course.execute("select * from class WHERE id = %s", [nid, ])
        result = course.fetchone()
        course.close()
        conn.close()
        print(result)
        return render(request,'studentmanagent/edit_class.html',{'result':result})
    else:
        pid = request.GET.get('nid')
        ptitle = request.POST.get('title')
        print(pid,ptitle)
        conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
        course = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # course.execute("update class set title = %s WHERE id = %s", [ptitle,pid,])
        course.execute("update class set title=%s  where id=%s", [ptitle, pid, ])
        conn.commit()
        course.close()
        conn.close()
        return redirect('/classes/')

def del_class(request):
    nid = request.GET.get('nid')
    conn = pymysql.connect(host='localhost', port=3306, user='kk', passwd='123', db='webdb', charset='utf8')
    course = conn.cursor(cursor=pymysql.cursors.DictCursor)
    course.execute("delete from class WHERE id = %s", [nid, ])
    conn.commit()
    course.close()
    conn.close()
    return redirect('/classes/')

