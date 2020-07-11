from django.urls import path
from . import views
from django.views.generic import TemplateView

# urls for general application
urlpatterns = [
	path ("", views.index , name ="ShopHome") ,
	path ("about/", views.about , name ="AboutUs"),
	path ("contact/", views.contact , name ="ContactUs"),
	path ("tracker/", views.tracker , name ="TrackingStatus"),
	path ("search/", views.search , name ="Search"),
	path ("shop/products/<int:myid>", views.productView , name ="ProductView"),
	path ("checkout/", views.checkout , name ="Checkout"),
	path("handlerequest",views.handlerequest, name='HandleRequest'),
	
	
	
]
# urls for authentications
urlpatterns += [

	path("signup/", views.signup, name = 'signup'),
	path("signin/", views.signin, name = 'signin'),
	path("signout/", views.signout, name = 'signout'),
	path('signin/reset-password', views.reset_password, name='reset-password'),
	# path('profile', views.profile, name='profile')
	path('profile', TemplateView.as_view(template_name='shop/profile.html')),
	path('profile/orders', views.orderList, name='orderList')
]

