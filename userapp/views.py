from django.core.serializers import serialize
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render



# Create your views here.
from django.views import View

from cart.cartmanager import SessionCartManager
from userapp.models import UserInfo, Area, Address
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
        red = request.GET.get('redirct', '')
        return render(request, 'login.html',{'redirect':red})

    def post(self, request):
        # 1.获取请求参数
        uname = request.POST.get('uname', '')
        pwd = request.POST.get('pwd', '')

        # 2.查询数据库中是否存在
        userList = UserInfo.objects.filter(uname=uname, pwd=pwd)
        red = request.POST.get('redirect', '')


        if userList:
            request.session['user'] = userList[0]
            if red == 'cart':
                # 将session中的购物项移动到数据库
                SessionCartManager(request.session).migrateSession2DB()

                return HttpResponseRedirect('/cart/queryAll/')

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


class AddressView(View):
    def get(self, request):
        user = request.session.get('user', '')
        # 获取当前登录用户的所有收货地址
        addrList = user.address_set.all()

        return render(request, 'address.html', {'addrList': addrList})

    def post(self, request):
        #获取请求参数
        aname = request.POST.get('aname', '')
        aphone = request.POST.get('aphone', '')
        addr = request.POST.get('addr', '')
        user = request.session.get('user', '')

        address = Address.objects.create(aname=aname, aphone=aphone, addr=addr,isdefault=(lambda count: True if count == 0 else False)(user.address_set.all().count()),userinfo=user)
        addrList = user.address_set.all()
        return render(request, 'address.html', {'addrList':addrList})


class LoadAreaView(View):
    def get(self, request):
        #获取请求参数
        pid = request.GET.get('pid', -1)
        pid = int(pid)
        # 根据父id查询区划信息
        areaList = Area.objects.filter(parentid=pid)

        # 进行序列化
        jareaList = serialize('json', areaList)

        return JsonResponse({'jareaList': jareaList})