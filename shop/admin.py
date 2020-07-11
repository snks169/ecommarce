from django.contrib import admin

# Register your models here.
from .models import Product , Contact, Orders, OrderUpdate ,Profile
admin.site.site_header = 'my awsome cart'

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Profile)

@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
	list_display = ('order_id','name','email','phone','user' )
	search_fields = (
		'order_id',
		'name',
		'phone',
		'email',
		'user',
		)
	
		

@admin.register(OrderUpdate)
class OrderUpdateAdmin(admin.ModelAdmin):
	list_display = ('order_id','update_desc')

