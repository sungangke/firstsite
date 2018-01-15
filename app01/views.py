
import pymysql
from django.shortcuts import render,redirect,HttpResponse
import json
#装饰器
def auth(func):
    def wrapper(request,*args,**kwargs):
        tk = request.COOKIES.get('ticket')
        if not tk:
            return redirect('/login/')
        ret = func(request,*args,**kwargs)
        return ret
    return wrapper

#配置登陆装饰器
@auth
def classes(request):
    #login 那里设置的cookie 跳转
    # tk = request.COOKIES.get('ticket')
    # if not tk:
    #     return  redirect('/login/')
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
    course.execute("delete from class WHERE id=%s", [nid, ])
    conn.commit()
    course.close()
    conn.close()
    return redirect('/classes/')

from untils import pymysqlhepler
def students(request):
    if request.method == "GET":
        student_list = pymysqlhepler.get_list("select student.id,student.name,student.class_id,class.title from student LEFT JOIN class ON student.class_id = class.id",[])
        class_list = pymysqlhepler.get_list("select id,title from CLASS",[])
        return render(request,'studentmanagent/students.html',{'student_list':student_list,'class_list':class_list})

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

def modal_add_class(request):
    title = request.POST.get('title')
    if len(title) > 0:
        pymysqlhepler.movde_list('insert into class(title) values(%s)',[title,])
        return HttpResponse('ok')
    else:
        return HttpResponse('班级标题不能为空')

def modal_edit_class(request):
    ret = {'status':True,'message':None}
    try:
        nid = request.POST.get('nid')
        content = request.POST.get('content')
        pymysqlhepler.movde_list("update class set title=%s WHERE id=%s",[content,nid])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)

    return  HttpResponse(json.dumps(ret))

def modal_add_student(request):
    ret = {'status': True, 'message': None}
    try:
        name = request.POST.get('name')
        class_id = request.POST.get('class_id')
        pymysqlhepler.movde_list("insert into student(name,class_id) VALUES (%s,%s)",[name,class_id,])
    except Exception as e:
        ret['status'] = False
        ret['message'] = str(e)
    return HttpResponse(json.dumps(ret))

def modal_edit_student(request):
    ret = {'status': True, 'message': None}
    try:
        studentId=request.POST.get('nid')
        studentName=request.POST.get('name')
        cls_Id=request.POST.get('class_id')
        pymysqlhepler.movde_list("update student set name=%s,class_id=%s WHERE id=%s",[studentName,cls_Id,studentId,])
    except Exception as e:
        ret['status']=False
        ret['message']=str(e)
    return HttpResponse(json.dumps(ret))

###多对多 老师表

def teachers(request):
    # teacher_list = pymysqlhepler.get_list('select id,name from teachers',[])
    teacher_list = pymysqlhepler.get_list(
        """
        SELECT teachers.id as tid,teachers.`name` ,class.title from teachers
        LEFT JOIN teacher2class ON teachers.id = teacher2class.teacher_id
        LEFT JOIN class ON class.id = teacher2class.class_id;
    """,[])
    result = {}
    for row in teacher_list:
        tid = row['tid']
        if tid in result:
            result[tid]['titles'].append(row['title'])
        else:
            result[tid]={'tid':row['tid'],'name':row['name'],'titles':[row['title'],]}
    return render(request,'studentmanagent/teacher.html',{'teacher_list':result.values()})

#添加老师
def add_teacher(request):
    if request.method=="GET":
        class_list = pymysqlhepler.get_list("select id,title from class",[])
        return  render(request,'studentmanagent/add_teacher.html',{'class_list':class_list})
    else:
        name= request.POST.get('name')
        class_ids = request.POST.getlist("class_ids")
        obj = pymysqlhepler.SqlHelper()
        teacher_id = obj.create('insert into teachers(NAME ) VALUES (%s)',[name,])
        # for cls_id in class_ids:
        #     pymysqlhepler.movde_list('insert into teacher2class(teacher_id,class_id) VALUES (%s,%s)',[teacher_id,cls_id])
        # 下面开始优化数据库，减少连接次数 在pymysqlhepler 创建新的类。然后使用新方法
        #第一种方法连接一次，提交多次，因为modify里面有commit
        # obj=pymysqlhepler.SqlHelper()
        # for cls_id in class_ids:
        #     obj.modify("insert into teacher2class(teacher_id,class_id) VALUES (%s,%s)",[teacher_id,cls_id])
        # obj.close()

        #连接一次，并且提交一次

        data_list = []
        for cls_id in class_ids:
            temp = (teacher_id,cls_id)
            data_list.append(temp)
        obj.multiple_modify("insert into teacher2class(teacher_id,class_id) VALUES (%s,%s)",data_list)
        obj.close()
        return redirect('/teachers/')


#编辑老师
def edit_teacher(request):
    if request.method=="GET":
        nid = request.GET.get('nid')
        obj = pymysqlhepler.SqlHelper()
        teacher_info = obj.get_one('select id,name from teachers WHERE id=%s',[nid,])
        class_id_list = obj.get_list("select class_id from teacher2class where teacher_id=%s",[nid,])
        class_list = obj.get_list("select id,title from class",[])
        print("老师信息： ",teacher_info)
        print("老师代课： " ,class_id_list)
        print("班级信息： " ,class_list)
        temp=[]
        for i in class_id_list:
            temp.append(i['class_id'])
        return render(request,'studentmanagent/edit_teacher.html',{
            'teacher_info':teacher_info,
            'class_id_list':temp,
            'class_list':class_list
        })
    else:
        nid = request.GET.get('nid')
        name = request.POST.get('name')
        class_id = request.POST.getlist('cls_ids')
        #更新老师信息
        obj = pymysqlhepler.SqlHelper()
        #更新老师
        obj.modify("update teachers set name=%s WHERE id=%s",[name,nid,])
        #更新老师和班级信息
        obj.modify("delete from teacher2class WHERE teacher_id=%s",[nid,])
        data_list=[]
        for cls_id in class_id:
            temp = (nid, cls_id)
            data_list.append(temp)
        obj.multiple_modify("insert into teacher2class(teacher_id,class_id) VALUES (%s,%s)", data_list)
        obj.close()

        return redirect('/teachers/')

#对话框添加老师
def get_all_class(request):
    obj=pymysqlhepler.SqlHelper()
    class_list = obj.get_list("select id,title from class",[])
    obj.close()
    return HttpResponse(json.dumps(class_list))

def modal_add_teacher(request):
    ret={'status':True,'message':None}
    try:
        name = request.POST.get('name')
        class_id_list = request.POST.getlist('class_id_list')
        obj = pymysqlhepler.SqlHelper()
        teacher_id = obj.create('insert into teachers(NAME ) VALUES (%s)', [name, ])
        data_list = []
        for cls_id in class_id_list:
            temp = (teacher_id, cls_id)
            data_list.append(temp)
        obj.multiple_modify("insert into teacher2class(teacher_id,class_id) VALUES (%s,%s)", data_list)
        obj.close()
    except Exception as e:
        ret['status'] = False
        ret['message'] = "处理失败"
    return HttpResponse(json.dumps(ret))

#########################后台管理
def layout(request):
    return render(request,'houtaiguanli/layout.html')

###登陆窗口
def login(request):
    if request.method == "GET":
        return render(request,'houtaiguanli/login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == 'ke' and pwd == '123':
            obj = redirect('/classes/')
            obj.set_cookie('ticket','dafadfafaf')
            return obj
        else:
            return render(request,'houtaiguanli/login.html')
