from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import *

# Create your views here.
from cart.cartmanager import *


class AddCartView(View):
    def post(self, request):
        # 在多级字典数据的时候，需要手动设置modified=True，实时地将数据存入到session对象中。
        request.session.modified = True
        flag = request.POST.get('flag', '')

        if flag == 'add':
            carManagerObj = getCartManger(request)
            #加入到购物车内
            carManagerObj.add(**request.POST.dict())
        elif flag == 'plus':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            # 修改商品的数量（添加）
            carManagerObj.update(step=1, **request.POST.dict())

        elif flag == 'minus':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            # 修改商品的数量（添加）
            carManagerObj.update(step=-1, **request.POST.dict())

        elif flag == 'delete':
            # 创建cartManager对象
            carManagerObj = getCartManger(request)
            # 逻辑删除购物车选项
            carManagerObj.delete(**request.POST.dict())
        return HttpResponseRedirect('/cart/queryAll/')

class CartListView(View):
    def get(self, request):
        carManagerObj = getCartManger(request)
        #查询所有信息
        cartList = carManagerObj.queryAll()

        return render(request, 'cart.html', {'cartList':cartList})


