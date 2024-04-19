from django.urls import path

from . import views

urlpatterns = [
    path('handleform', views.handle_form, name='form'),
    path('', views.index, name='index'),
    path('new/', views.new_user, name='new_user'),
    path('createUser/', views.create_user, name='create_user')
    
    #path('handleform', views.handle_form, name='form'),
]
