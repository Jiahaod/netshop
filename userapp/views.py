from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render



# Create your views here.
from django.views import View
from userapp.models import UserInfo
from utils.code import gene_code


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        user = UserInfo.objects.create(uname=uname, pwd=pwd)
        if user:
            #将用户信息存放到session对象中
            request.session['user'] = user
            return HttpResponseRedirect('/user/center/')

        return HttpResponseRedirect('/user/register/')


class CheckUnameView(View):
    def get(self, request):
        uname = request.GET.get('uname', '')
        #根据用户名去数据库中查
        userList = UserInfo.objects.filter(uname=uname)

        flag = False
        if userList:
            flag = True

        return JsonResponse({'flag':flag})

class CenterView(View):
    def get(self,request):
        return render(request,'center.html')


class LogoutView(View):
    def post(self, request):
        #删除session中登录用户信息
        if 'user' in request.session:
            del request.session['user']

        return JsonResponse({'delflag':True})


class LoginView(View):
    def get(self, request):

        return render(request, 'login.html')

    def post(self, request):
        # 1.获取请求参数
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        # 2.查询数据库中是否存在
        userList = UserInfo.objects.filter(uname=uname, pwd=pwd)

        if userList:
            request.session['user'] = userList[0]
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')

class LoadCodeView(View):
    def get(self, request):
        img, str = gene_code()
        request.session['sessionCode'] = str
        return HttpResponse(img, content_type='image/png')


class CheckCodeView(View):
    def get(self,request):
        #获取输入框中的验证码
        code = request.GET.get('code','')

        #获取生成的验证码
        sessionCode = request.session.get('sessionCode',None)

        #比较是否相等
        flag = code == sessionCode

        return JsonResponse({'checkFlag':flag})