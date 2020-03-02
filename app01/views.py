from django.shortcuts import render,HttpResponse,redirect
from django.core.paginator import Paginator,EmptyPage
from app01.models import Publish,Author,Book,UserInfo
from app01.myforms import *
import json
import re
import datetime
# Create your views here.

# 主页函数
def home(request, role):
    book_list = Book.objects.all()
    author_list = Author.objects.all()
    publish_list = Publish.objects.all()
    use_author_list = []
    for author in author_list:
        pk = author.nid
        for book_obj in book_list:
            author = book_obj.authors.filter(pk=pk).first()
            if author:
                use_author_list.append(author)
                break
    username = request.session.get("username")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_visit_time = request.session.get("last_visit_time", now)
    # 分页器
    if role == 'book':
        paginator = Paginator(book_list, 10)
    elif role == 'author':
        paginator = Paginator(author_list, 10)
    else:
        paginator = Paginator(publish_list, 10)
    current_page_num = int(request.GET.get("page", 1))
    if paginator.num_pages > 11:
        if current_page_num - 5 < 1:
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)

        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
    try:
        if role == 'book':
            book_list = paginator.page(current_page_num)
        elif role == 'author':
            author__list = paginator.page(current_page_num)
        else:
            publish_list = paginator.page(current_page_num)
    except EmptyPage as e:
        if role == 'book':
            book_list = paginator.page(1)
        elif role == 'author':
            author__list = paginator.page(1)
        else:
            publish_list = paginator.page(1)

    return locals()
# 书籍列表
def book_home(request):
    book_list = Book.objects.all().order_by("nid")
    author_list = Author.objects.all()
    publish_list = Publish.objects.all()
    username = request.session.get("username")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_visit_time = request.session.get("last_visit_time", now)
    # 分页器
    paginator = Paginator(book_list, 10)
    current_page_num = int(request.GET.get("page", 1))
    if paginator.num_pages > 11:
        if current_page_num - 5 < 1:
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)

        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
    try:
        book_list = paginator.page(current_page_num)
    except EmptyPage as e:
        book_list = paginator.page(1)
    return render(request, 'book_home.html', locals())
# 作者列表
def book_author(request):
    book_list = Book.objects.all()
    author_list = Author.objects.all().order_by("nid")
    publish_list = Publish.objects.all()
    use_author_list = []
    username = request.session.get("username")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_visit_time = request.session.get("last_visit_time", now)
    # 分页器
    paginator = Paginator(author_list, 10)
    current_page_num = int(request.GET.get("page", 1))
    if paginator.num_pages > 11:
        if current_page_num - 5 < 1:
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)

        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
    try:
        author_list = paginator.page(current_page_num)
        for author in author_list:
            pk = author.nid
            for book_obj in book_list:
                author = book_obj.authors.filter(pk=pk).first()
                if author:
                    use_author_list.append(author)
                    break
    except EmptyPage as e:
        author_list = paginator.page(1)
        for author in author_list:
            pk = author.nid
            for book_obj in book_list:
                author = book_obj.authors.filter(pk=pk).first()
                if author:
                    use_author_list.append(author)
                    break
    return render(request, 'book_author.html', locals())

# 出版社列表
def book_publish(request):
    book_list = Book.objects.all()
    publish_list = Publish.objects.all().order_by("nid")
    username = request.session.get("username")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    last_visit_time = request.session.get("last_visit_time", now)
    # 分页器
    paginator = Paginator(publish_list, 10)
    current_page_num = int(request.GET.get("page", 1))
    if paginator.num_pages > 11:
        if current_page_num - 5 < 1:
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)

        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
    try:
        publish_list = paginator.page(current_page_num)
    except EmptyPage as e:
        publish_list = paginator.page(1)
    return render(request, 'book_publish.html', locals())



# 登录
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            request.session["is_login"] = True
            request.session["username"] = form.cleaned_data.get('name')
            request.session["last_visit_time"] = now
            return redirect('/book/book_home/')
        else:
            errors = form.errors.get("__all__")
            return render(request, 'login.html', locals())
    form = LoginForm()
    return render(request, 'login.html', locals())
# 注册
def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data
            user = UserInfo.objects.create(name=user.get('name'), pwd=user.get('pwd'), email=user.get('email'), tel=user.get('tel'))
            return redirect('/login/')
        else:
            errors = form.errors.get("__all__")
            return render(request, 'register.html', locals())
    form = UserForm()
    return render(request, 'register.html', locals())
# 注销
def logout(request):
    request.session.flush()
    return redirect("/login/")


# 查看作者书籍
def check_author_book(request,id):
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    book_all = Book.objects.all()
    book_list = []
    for book_obj in book_all:
        if book_obj.authors.filter(pk=id).first():
            book_list.append(book_obj)
    author_name = Author.objects.filter(pk=id).first().name
    # 分页器
    paginator = Paginator(book_list, 10)
    current_page_num = int(request.GET.get("page", 1))
    if paginator.num_pages > 11:
        if current_page_num - 5 < 1:
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)

        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
    try:
        book_list = paginator.page(current_page_num)
    except EmptyPage as e:
        current_page = paginator.page(1)
    return render(request, 'author_check_book.html', locals())
# 查看出版社书籍
def check_publish_book(request,id):
    publish_list = Publish.objects.all()
    author_list = Author.objects.all()
    book_list = Book.objects.filter(publish=id).all().order_by('nid')
    publish_name = Publish.objects.filter(pk=id).first().name
    # 分页器
    paginator = Paginator(book_list, 10)
    current_page_num = int(request.GET.get("page", 1))
    if paginator.num_pages > 11:
        if current_page_num - 5 < 1:
            page_range = range(1, 12)
        elif current_page_num + 5 > paginator.num_pages:
            page_range = range(paginator.num_pages - 10, paginator.num_pages + 1)

        else:
            page_range = range(current_page_num - 5, current_page_num + 6)
    else:
        page_range = paginator.page_range
    try:
        book_list = paginator.page(current_page_num)
    except EmptyPage as e:
        current_page = paginator.page(1)
    return render(request, 'check_book.html', locals())


# 添加书籍
def add_book(request):
    try:
        res = {}
        if request.method == 'POST':
            title = request.POST.get('title')
            if not title:
                res['res'] = 11
                res['error'] = '书名不能为空'
                return HttpResponse(json.dumps(res))
            book_obj = Book.objects.filter(title=title).first()
            if book_obj:
                res['res'] = 10
                res['error'] = '书名已存在'
                return HttpResponse(json.dumps(res))
            price = request.POST.get('price')
            price = re.search('^(\d)+(\.)?(\d){0,2}$', price)
            if price:
                price = price.group()
                if not isinstance(eval(price),float) and (not price.isdigit()):
                    res['res'] = 21
                    res['error'] = '请输入正确的价格，支持两位小数！'
                    return HttpResponse(json.dumps(res))
            else:
                res['res'] = 20
                res['error'] = '请输入正确的价格，支持两位小数！'
                return HttpResponse(json.dumps(res))
            data = request.POST.get('publishDate')
            if not data:
                res['res'] = 30
                res['error'] = '时间不能为空！'
                return HttpResponse(json.dumps(res))
            publish_id = request.POST.get('publish_id')
            author_id_list = request.POST.getlist('author_id_list')
            if len(author_id_list) == 0:
                res['res'] = 40
                res['error'] = '作者不能为空'
                return HttpResponse(json.dumps(res))

            book_obj = Book.objects.create(title=title,price=price,publishDate=data,publish_id=publish_id)
            book_obj.authors.add(*author_id_list)
            res['res'] = 0
            return HttpResponse(json.dumps(res))

    except Exception as e:
        print(e)
        res['res'] = 50
        res['error'] = '未知错误'
        return HttpResponse(json.dumps(res))
# 编辑书籍
def change_book(request,id):
    try:
        book_obj = Book.objects.filter(pk=id).first()
        res = {}
        if request.method == 'POST':
            price = request.POST.get('price')
            price = re.search('^(\d)+(\.)?(\d){0,2}$', price)
            if price:
                price = price.group()
                if not isinstance(eval(price),float) and (not price.isdigit()):
                    res['res'] = 1
                    res['error'] = '请输入正确的价格，支持两位小数！'
                    return HttpResponse(json.dumps(res))
            else:
                res['res'] = 1
                res['error'] = '请输入正确的价格，支持两位小数！'
                return HttpResponse(json.dumps(res))
            data = request.POST.get('publishDate')
            publish_id = request.POST.get('publish_id')
            author_id_list = request.POST.getlist('author_id_list')
            res['res_book'] = Book.objects.filter(pk=id).update(price=price,publishDate=data,publish_id=publish_id)
            res['res_author'] = book_obj.authors.set(author_id_list)
            if res['res_book'] == 1:
                res['res'] = 0
                return HttpResponse(json.dumps(res))
            else:
                res['res'] = 1
                res['error'] = "更新表出错"
                return HttpResponse(json.dumps(res))

    except Exception as e:
        res['res'] = 1
        res['error'] = e
        return HttpResponse(json.dumps(res))
# 删除书籍
def delete_book(request,id):
    Book.objects.filter(pk=id).delete()
    return redirect('/book/book_home/')


# 编辑作者
def change_author(request,id):
    try:
        author_name = Author.objects.filter(pk=id).first().name
        res = {}
        if request.method == 'POST':
            name = request.POST.get('name')
            if not name:
                res['res'] = 10
                res['error'] = '作者名不能为空'
                return HttpResponse(json.dumps(res))
            author_obj = Author.objects.filter(name=name).first()
            if author_obj and author_obj.name != author_name:
                res['res'] = 11
                res['error'] = '作者名已存在'
                return HttpResponse(json.dumps(res))
            age = request.POST.get('age')
            if not age.isdigit():
                res['res'] = 20
                res['error'] = '年龄要输入整数'
                return HttpResponse(json.dumps(res))
            res['res_author'] = Author.objects.filter(pk=id).update(name=name, age=age)
            # res['res_author'] = book_obj.authors.set(author_id_list)
            res['res'] = 0
            return HttpResponse(json.dumps(res))

    except Exception as e:
        res['res'] = 1
        res['error'] = e
        return HttpResponse(json.dumps(res))
# 新增作者
def add_author(request):
    try:
        if request.method == 'POST':
            res = {}
            name = request.POST.get('name')
            if not name:
                res['res'] = 10
                res['error'] = '作者名不能为空'
                return HttpResponse(json.dumps(res))
            author_obj = Author.objects.filter(name=name).first()
            if author_obj :
                res['res'] = 11
                res['error'] = '作者名已存在'
                return HttpResponse(json.dumps(res))
            age = request.POST.get('age')
            if not age.isdigit():
                res['res'] = 20
                res['error'] = '年龄要输入整数'
                return HttpResponse(json.dumps(res))
            Author.objects.create(name=name, age=age)
            res['res'] = 0
            return HttpResponse(json.dumps(res))

    except Exception as e:
        res['res'] = 1
        res['error'] = e
        return HttpResponse(json.dumps(res))
# 删除作者
def delete_author(request,id):
    Author.objects.filter(pk=id).delete()
    return redirect('/book/book_author/')


# 编辑出版社
def change_publish(request,id):
    try:
        publish_name = Publish.objects.filter(pk=id).first().name
        res = {}
        if request.method == 'POST':
            name = request.POST.get('name')
            if not name:
                res['res'] = 10
                res['error'] = '出版社名不能为空'
                return HttpResponse(json.dumps(res))
            publish_obj = Publish.objects.filter(name=name).first()
            if publish_obj and publish_obj.name != publish_name:
                res['res'] = 11
                res['error'] = '出版社名已存在'
                return HttpResponse(json.dumps(res))
            city = request.POST.get('city')
            if not city:
                res['res'] = 20
                res['error'] = '城市不能为空'
                return HttpResponse(json.dumps(res))
            email = request.POST.get('email')
            if not email:
                res['res'] = 30
                res['error'] = '邮箱不能为空'
                return HttpResponse(json.dumps(res))
            form = PublishForm({'email': email})
            if not form.is_valid():
                res['res'] = 31
                res['error'] = '邮箱格式不正确'
                return HttpResponse(json.dumps(res))
            res['res_publish'] = Publish.objects.filter(pk=id).update(name=name, city=city, email=email)
            res['res'] = 0
            return HttpResponse(json.dumps(res))

    except Exception as e:
        print(e)
        res['res'] = 1
        res['error'] = "未知错误"
        return HttpResponse(json.dumps(res))
# 新增出版社
def add_publish(request):
    try:
        res = {}
        if request.method == 'POST':
            name = request.POST.get('name')
            if not name:
                res['res'] = 10
                res['error'] = '出版社名不能为空'
                return HttpResponse(json.dumps(res))
            publish_obj = Publish.objects.filter(name=name).first()
            if publish_obj:
                res['res'] = 11
                res['error'] = '出版社名已存在'
                return HttpResponse(json.dumps(res))
            city = request.POST.get('city')
            if not city:
                res['res'] = 20
                res['error'] = '城市不能为空'
                return HttpResponse(json.dumps(res))
            email = request.POST.get('email')
            if not email:
                res['res'] = 30
                res['error'] = '邮箱不能为空'
                return HttpResponse(json.dumps(res))
            form = PublishForm({'email': email})
            if not form.is_valid():
                res['res'] = 31
                res['error'] = '邮箱格式不正确'
                return HttpResponse(json.dumps(res))
            Publish.objects.create(name=name, city=city, email=email)
            res['res'] = 0
            return HttpResponse(json.dumps(res))

    except Exception as e:
        print(e)
        res['res'] = 1
        res['error'] = "未知错误"
        return HttpResponse(json.dumps(res))
# 删除出版社
def delete_publish(request,id):
    Publish.objects.filter(pk=id).delete()
    return redirect('/book/book_publish/')


# 数据库创建测试数据
def test(request):
    author_list = []
    publish_list = []
    # 创建作者和出版社
    for i in range(100):
        author = Author(name="作者%s" % i, age=i)
        author_list.append(author)

        if i % 2:
            publish = Publish(name="出版社%s" % i, city='北京', email="bj%s@bj.com" % i)
        else:
            publish = Publish(name="出版社%s" % i, city='浙江', email="zj%s@zj.com" % i)
        publish_list.append(publish)
    Author.objects.bulk_create(author_list)
    Publish.objects.bulk_create(publish_list)

    # 创建书籍
    for i in range(80):
        if i % 2:
            book = Book.objects.create(title='三国%s' % i, price=i+10, publishDate='2019-11-11', publish_id=i)
            book.authors.add(*[1, i+1])
        else:
            book = Book.objects.create(title='三国%s' % i, price=i+22, publishDate='2019-12-12', publish_id=2)
            book.authors.add(*[2, i+2])
    return redirect('/book/book_home/')

