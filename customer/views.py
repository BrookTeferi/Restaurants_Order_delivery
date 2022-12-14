from customer.models import Customer
from order.models import Order
from products.models import Product
# from django.contrib.auth.models import User

from django.contrib import messages
from customer.forms import CustomerModelForm
from customer.filters import CustomerFilter
from django.contrib import messages
from django.utils import timezone
from django.views.generic import ListView,DetailView#for pagination
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template.loader import render_to_string

from django.db.models import Q
from django.contrib.auth.decorators import login_required


		
@login_required(login_url = '/user/login/')     
def index(request):
	form = CustomerModelForm()
	customers=Customer.objects.all().order_by("-id")
	myFilter = CustomerFilter(request.GET,queryset=customers)
	customers = myFilter.qs#for searchng
	
	#pagination logic
	customer_count = customers.count()
	  

	   
	page = request.GET.get('page', 1)#means page  number 1
	
	# if page and page.isdigit():
	#     page = int(page)
	# else:
	#     page = 5
		
	# paginator = Paginator(customers, 5)#5 data per page
	paginator = Paginator(customers, 10)
  
	try:
		customers = paginator.page(page)
	except PageNotAnInteger:
		customers = paginator.page(1)
	except EmptyPage:
		#if page is out of range show last page
		customers = paginator.page(paginator.num_pages)

	

	context={
		'customers':customers,#this is for both pagination and table list use(blc table list also should support pagination.so dont pass data for list separately)
  		
    	'myFilter':myFilter,
		'form':form,'page':page,
		'customer_count':customer_count,
		'start': customers.start_index(),
		'end': customers.end_index(),
		}
	return render(request,'customers/copindex.html',context)



#I use function base view but use class base view to inherit index.I am just copying index code 
def search(request):
	data = dict()
	field_value = request.GET.get('query')#grab the input value
	print(field_value)
	
	# products = Product.objects.all()
	# myFilter = ProductFilter(request.GET,queryset=products)
	# products = myFilter.qs
 
	if field_value:
		customers = Customer.objects.filter(
	  
											Q(name__contains=field_value)
										   |Q(email__icontains=field_value) 
										   | Q(contact__contains=field_value)  
										   |Q(date_created__contains=field_value)                      
										   )
	
		context = {'customers': customers}
		data['html_list'] = render_to_string('customers/get_search_customers.html',context,request=request)
		return JsonResponse(data)
	else:
		customers = Customer.objects.all()
		context = {'customers': customers}
		data['html_list'] = render_to_string('customers/get_search_customers.html',context,request=request)
		return JsonResponse(data)





def create(request):    
	if request.method=="POST":
		form=CustomerModelForm(request.POST)
		if form.is_valid():
			cid =request.POST['cusid']
			name=request.POST.get("name")
			email=request.POST.get("email")
			contact=request.POST.get("contact")
		  
			
			if(cid==''):
				customer=Customer(name=name,email=email,contact=contact)
			else:
				customer=Customer(id = cid,name=name,email=email,contact=contact)
				
			customer.save()
			prod=Customer.objects.values()
			# print(prod,"--------------------------")
			customer_data =list(prod)
			
			return JsonResponse({'status':'Save','customer_data':customer_data,'message':'Customer is successfully submitted'},safe=False)
		else:
			return JsonResponse({'status':0},safe=False)
	   
  

def edit(request):
    if request.method=="POST":
        id=request.POST.get('cid')
        print(id)
        customer=Customer.objects.get(pk=id)
        customer_data={"id":customer.id,"name":customer.name,"email":customer.email, "contact":customer.contact}
	
        return JsonResponse(customer_data,safe=False)


	
def delete(request):
    if request.method=="POST":
        id=request.POST.get('cid')
        pi=Customer.objects.get(pk=id)
        pi.delete()
	  
        return JsonResponse({'status':1,'message':'Customer is successfully deleted'},safe=False)
    else:
        return JsonResponse({'status':0,'message':'Failed to delete data'},safe=False) 

   


def cus_ord_view(request, cid):
	# order = Order.objects.filter(customer__first_name="Shankar") 
	# -->I am retrieving  the order the  particular person 
 
	customer = get_object_or_404(Customer,pk=cid) #use to get beautiful error -u can also use below
	# customer = Customer.objects.get(pk = cid)#return a particular customer name according to choosen primary key
	orders = customer.order_set.all()#particular customer ko particular order select garxa--It is possible with customer id
	#here order in  order_set is attribute 
	#Order ma Customer is foreign key so ot os possible to use order_set with customer
	order_count = orders.count()
	order_count = orders.count()    
	customer_total_order_price=0.00
	
	for order in customer.order_set.all():
		per_total_price = float(order.product.price) * order.quantity
		# customer.per_total = per_total_price--to get the price of respective products
		#return value of first product i.e first row
		customer_total_order_price += per_total_price
		
	
 
	context = {'customer_total_price':customer_total_order_price,'customers':customer, 'orders':orders, 'order_count':order_count,'order_num':order_count}
	return render(request,'customers/orderview.html',context)

