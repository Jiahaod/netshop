from django.http import HttpResponse, JsonResponse
from django.shortcuts import render



# Create your views here.
from django.views import View

from userapp.models import UserInfo


class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        user = UserInfo.objects.create(uname=uname, pwd=pwd)
        if user:

            return HttpResponse('注册成功')
        return HttpResponse('注册失败')


class CheckUnameView(View):
    def get(self, request):
        uname = request.GET.get('uname', '')
        #根据用户名去数据库中查
        userList = UserInfo.objects.filter(uname=uname)

        flag = False
        if userList:
            flag = True

        return JsonResponse({'flag':flag})
