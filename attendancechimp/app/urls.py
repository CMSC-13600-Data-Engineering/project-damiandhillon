from django.urls import path

from . import views

urlpatterns = [
    path('handleform', views.handle_form, name='form'),
    path('', views.index, name='index'),
    path('create_user', views.new_user, name='create_user')
    #path('handleform', views.handle_form, name='form'),
]
