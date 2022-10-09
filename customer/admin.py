from django.contrib import admin
from customer.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display=['name','email','contact','date_created']
    
    