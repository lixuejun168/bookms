"""bookms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from app01 import views
urlpatterns = [
    path('admin/', admin.site.urls),
    # 主页
    re_path(r'book/book_home/$', views.book_home),
    re_path(r'book/book_author/$', views.book_author),
    re_path(r'book/book_publish/$', views.book_publish),

    # 登录
    re_path(r'login/$', views.login),
    # 注册
    re_path(r'register/$', views.register),
    # 注销
    re_path(r'logout/$', views.logout),

    # 查看出版社书籍
    re_path(r'book/(\d+)/check_publish_book/$', views.check_publish_book),
    # 查看作者书籍
    re_path(r'book/(\d+)/check_author_book/$', views.check_author_book),

    # 书籍
    re_path(r'book/add_book/$', views.add_book),
    re_path(r'book/(\d+)/change_book/$', views.change_book),
    re_path(r'book/(\d+)/delete_book/$', views.delete_book),
    # 作者
    re_path(r'book/add_author/$', views.add_author),
    re_path(r'book/(\d+)/change_author/$', views.change_author),
    re_path(r'book/(\d+)/delete_author/$', views.delete_author),
    # 出版社
    re_path(r'book/add_publish/$', views.add_publish),
    re_path(r'book/(\d+)/change_publish/$', views.change_publish),
    re_path(r'book/(\d+)/delete_publish/$', views.delete_publish),

    # 创建初始测试数据
    re_path(r'test/$', views.test),
]
