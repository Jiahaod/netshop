# -*- coding: utf-8 -*-
import jsonpickle
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from cart.cartmanager import getCartManger
from cart.models import CartItem
from goods.models import Inventory
from utils import alipay
from order.models import Order, OrderItem
from userapp.models import Address
from utils.alipay import AliPay


class ToOrderView(View):
    def get(self,request):
        #获取请求参数
        cartitems = request.GET.get('cartitems','')

        #判断用户是否登录
        if not request.session.get('user'):
            return render(request,'login.html',{'cartitems':cartitems,'redirect':'order'})

        return HttpResponseRedirect('/order/order.html?cartitems='+cartitems)


class OrderListView(View):
    def get(self,request):
        #获取请求参数
        cartitems = request.GET.get('cartitems','')
        #将json字符串转化为python对象列表
        cartitemList = jsonpickle.loads("["+cartitems+"]")
        print(cartitems)
        print(cartitemList)
        # 将python对象列表转换成CartItem对象列表
        cartitemObjList = [getCartManger(request).get_cartitems(**item) for item in cartitemList if item]
        print(cartitemObjList)
        # 获取用户的默认收货地址
        address = request.session.get('user').address_set.get(isdefault=True)

        # 获取支付总金额
        totalPrice = 0
        for cm in cartitemObjList:
            totalPrice += cm.getTotalPrice()

        return render(request, 'order.html',
                      {'cartitemObjList': cartitemObjList, 'address': address, 'totalPrice': totalPrice})

alipay = AliPay(appid='2021000118682302', app_notify_url='http://127.0.0.1:8000/order/checkPay/', app_private_key_path='order/keys/my_private_key.txt',
                 alipay_public_key_path='order/keys/alipay_public_key.txt', return_url='http://127.0.0.1:8000/order/checkPay/', debug=True)


class ToPayViews(View):
    def get(self,request):
        #1、插入Order表中数据
        import uuid, datetime
        data = {
            'out_trade_num': uuid.uuid4().hex,
            'order_num': datetime.datetime.today().strftime('%Y%m%d%H%M%S'),
            'payway': request.GET.get('payway'),
            'address': Address.objects.get(id=request.GET.get('address', '')),
            'user': request.session.get('user', '')
        }
        orderObj = Order.objects.create(**data)
        #print
        #(request.GET.get('cartitems', ''), '==========================')

        cartitems = jsonpickle.loads(request.GET.get('cartitems'))

        print(cartitems)

        orderItemList = [OrderItem.objects.create(order=orderObj, **item) for item in cartitems if item]

        totalPrice = request.GET.get('totalPrice')[1:]

        # 3.获取扫码支付的页面
        params = alipay.direct_pay(subject='京东超市', out_trade_no=orderObj.out_trade_num, total_amount=str(totalPrice))

        # 拼接请求地址
        url = alipay.gateway + '?' + params

        return HttpResponseRedirect(url)


class CheckPayView(View):
    def get(self,request):
        #校验是否支付成功（验签的过程）
        params = request.GET.dict()
        #获取签名
        sign = params.pop('sign')

        if alipay.verify(params, sign):
            #修改订单表中的支付状态
            out_trade_no = params.get('out_trade_no','')
            order = Order.objects.get(out_trade_num=out_trade_no)
            order.status = u'待发货'
            order.save()

            #修改库存
            orderitemList = order.orderitem_set.all()
            [Inventory.objects.filter(goods_id=item.goodsid,size_id=item.sizeid,color_id=item.colorid).update(count=F('count')-item.count) for item in orderitemList if item]

            # 修改购物表
            [CartItem.objects.filter(goodsid=item.goodsid,sizeid=item.sizeid,colorid=item.colorid).delete() for item in orderitemList if item]


            return HttpResponse('支付成功！')

        return HttpResponse('支付失败！')
