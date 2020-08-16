from django.shortcuts import render

# Create your views here.
from django.views import View

from goods.models import *





class IndexView(View):
    def get(self, request, cid = 2):
        cid = int(cid)
        #所有类别
        categorys = Category.objects.all().order_by('id')
        #该类别的东西
        Goods.objects.filter(category_id = cid)
        return render(request, 'index.html')