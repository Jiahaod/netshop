from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View

from goods.models import *
import math




class IndexView(View):
    def get(self, request, cid = 1, num = 1):
        cid = int(cid)
        num = int(num)

        #所有类别
        categorys = Category.objects.all().order_by('id')
        #该类别的东西
        goodList = Goods.objects.filter(category_id = cid).order_by('id')
        #每页8页
        pager = Paginator(goodList, 8)
        #当前页的数据
        page_goodsList = pager.page(num)
        begin = (num - int(math.ceil(10.0/2)))

        if begin < 1:
            begin = 1

        end = begin + 9

        if end > pager.num_pages:
            end = pager.num_pages

        if end <= 10:
            begin = 1
        else:
            begin = end - 9

        pagelist = range(begin, end+1)
        return render(request, 'index.html', {'categorys':categorys, 'goodsList':page_goodsList,'currentCid':cid,'pagelist':pagelist,'currentNum':num})


class DetailView(View):
    def get(self, request, goodsid):
        goodsid = int(goodsid)

        #查询goodsid查询商品内容
        goods = Goods.object.get(goods_id = goodsid)

        return render(request, 'detail.html', {'goods':goods})