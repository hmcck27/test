from django.db import models
from django.conf import settings
##from posts.models import Review
# Create your models here.

class Brand(models.Model) :
    name = models.CharField(max_length = 100)
    is_partner= models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

## update_sale_prices를 통해서 Brand를 참조하는
# item들을 역참조한다. 그후 item들의 판매가를 정가-amount로 조정한다.
# 이때 조건으로 100000 미만인 경우만!   
    def update_sale_prices(self,amount) :
        qs = self.item_set.all()
        for item in qs :
            if item.original_price < 100000 :
                item.sale_price = item.original_price - amount
                item.save()

    

class Item(models.Model) :
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    purchase_url = models.URLField()
    image_url = models.URLField()
    is_soldout = models.BooleanField(default = False)
    original_price = models.PositiveIntegerField()
    sale_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add = True)

    
    def __str__(self):
        return self.name
## update_review_availability를 통해서 제품이 soldout이면
# 이 제품의 review의 is_purchasable을 다 False로 바꾼다.
    def update_review_availability(self) :
        if self.is_soldout == True :
            review_list = self.review_set.all()
            review_list.update(is_purchasable = False)
        