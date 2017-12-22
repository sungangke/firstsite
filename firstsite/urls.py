"""firstsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.shortcuts import HttpResponse,render,redirect
# import pymysql
from app01 import views
# conn = pymysql.connect(host='localhost',port=3306,user='kk',passwd='123',db='webdb',charset='utf8')
# course=conn.cursor(cursor=pymysql.cursors.DictCursor)
#
#
# def login(request):
#     if request.method == "GET":
#         return render(request, 'first/login.html')
#     else:
#         u=request.POST.get('username')
#         p=request.POST.get('password')
#         course.execute("select * from adminuser")
#         res1 = course.fetchall()
#         for row in res1:
#             if u == row['name'] and p == row['passwd']:
#                 return redirect('/userlist/')
#             else:
#                 return render(request, 'first/login.html')
#
# def userlist(request):
#     course.execute("select * from userlist")
#     res2 = course.fetchall()
#     # print(res2)
#     for a in res2:
#         # print(a)
#     return render(request, 'first/userlist.html', {'res2':res2})
    # return HttpResponse('<input type="text">')
    # return HttpResponse('login')
urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    # url(r'^login/', login),
    # url(r'^userlist/', userlist),
    url(r'^classes/', views.classes),
    url(r'^add_class/', views.add_class),
    url(r'^edit_class/', views.edit_class),
    url(r'^del_class/', views.del_class),
    url(r'^students/', views.students),
    url(r'^add_student/', views.add_student),
    url(r'^ed_student/', views.ed_student),
]
