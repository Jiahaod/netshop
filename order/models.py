from django.db import models

# Create your models here.

from userapp.models import Address, UserInfo


class Order(models.Model):
    out_trade_num = models.UUIDField()
    order_num = models.CharField(max_length=50)
    trade_no = models.CharField(max_length=120)
    status = models.CharField(max_length=20)
    payway = models.CharField(max_length=20,default='alipay')
    address = models.ForeignKey(Address, models.CASCADE)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)



class OrderItem(models.Model):
    goodsid = models.PositiveIntegerField()
    colorid = models.PositiveIntegerField()
    sizeid = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    order = models.ForeignKey(Order,models.CASCADE)
