from django.urls import path

from analog import views

urlpatterns=[
    path('',views.home)
]