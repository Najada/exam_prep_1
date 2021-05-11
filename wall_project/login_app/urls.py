from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    # trips urls
    path('travels/add', views.add),
    path('travels/save', views.save),
    path('travels/<int:id>/join', views.join),
    path('travels/destination/<int:id>', views.destination),
]