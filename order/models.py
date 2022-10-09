from django.db import models
from customer.models import Customer
from products.models import Product
class Order(models.Model):
    status=(
        ('Pending','Pending'),
        ('Delivered','Delivered'),
        ('Out for delivery','out for delivery')   
    )

    id=models.IntegerField(primary_key=True)
    customer_id=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    product_id=models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
    created_at=models.DateTimeField(max_length=50,null=True,auto_now=True)
    status=models.CharField(max_length=100,null=True,choices=status)
    quantity = models.IntegerField(default=1,blank=False)
    total_price = models.DecimalField(max_digits=5,decimal_places=2,default=0)
    class Meta:
        db_table='tbl_order'

    def save(self,*args,**kwargs):
    	super().save(*args,**kwargs)
    @property
    def get_total_item_price(self):#for particular product order total
        return self.quantity * self.product.price