
import pymysql
from django.shortcuts import render,redirect,HttpResponse

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

from untils import pymysqlhepler
def students(request):
    if request.method == "GET":
        student_list = pymysqlhepler.get_list("select student.id,student.name,class.title from student LEFT JOIN class ON student.class_id = class.id",[])
        return render(request,'studentmanagent/students.html',{'student_list':student_list})

def add_student(request):
    if request.method == "GET":
        class_list = pymysqlhepler.get_list("select id,title from class",[])
        return render(request,'studentmanagent/add_student.html',{'class_list':class_list})
    else:
        nid = request.POST.get('stu_name')
        title = request.POST.get('cls_sel')
        print(nid,title)
        pymysqlhepler.movde_list("insert into student(name,class_id) VALUES (%s,%s)",[nid,title])
        return redirect('/students/')

def ed_student(request):
    if request.method == "GET":
        nid = request.GET.get('nid')
        stu_name = pymysqlhepler.get_one("select * from student WHERE id=%s",[nid,])
        class_name = pymysqlhepler.get_list("select id,title from class",[])

        return render(request,'studentmanagent/ed_student.html',{'class_name':class_name,'stu_name':stu_name})

    else:
        nid = request.GET.get('nid')
        st_name = request.POST.get('st_n')
        cls_name = request.POST.get('class_name')
        pymysqlhepler.movde_list("update student set name=%s, class_id=%s WHERE id=%s",[st_name,cls_name,nid])
        return redirect('/students/')

