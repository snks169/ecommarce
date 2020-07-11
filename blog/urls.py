from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path("", views.index, name="blogHome"),
    path("blogpost/<int:id>", views.blogpost, name="blogpost"),
    path('ajax', TemplateView.as_view(template_name='blog/ajax.html')),
]
 