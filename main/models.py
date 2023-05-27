from django.db import models

class Sejong_b(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True)
    cate1 = models.TextField(null=True)
    cate2 = models.TextField(null=True)
    cate3 = models.TextField(null=True)
    catemix = models.TextField(null=True)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    type = models.TextField(null=True)
    star = models.FloatField(null=True)
    qty = models.TextField(null=True)
    keyword = models.TextField(null=True)
    review = models.TextField(null=True)
    positive = models.TextField(null=True)
    
    class Meta:
        db_table = 'Sejong_b'
        managed = False

class Sejong_A(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True)
    cate1 = models.TextField(null=True)
    cate2 = models.TextField(null=True)
    cate3 = models.TextField(null=True)
    catemix = models.TextField(null=True)
    dong = models.TextField(null=True)
    lon = models.FloatField(null=True)
    lat = models.FloatField(null=True)
    store_type = models.TextField(null=True)
    star = models.FloatField(null=True)
    review_ori = models.TextField(null=True)
    review_qty = models.FloatField(null=True)
    menu_keyword = models.TextField(null=True)
    address = models.TextField(null=True)
    call = models.TextField(null=True)
    review_okt = models.TextField(null=True)
    positive = models.FloatField(null=True)
    
    class Meta:
        db_table = 'Sejong_A'
        managed = False
