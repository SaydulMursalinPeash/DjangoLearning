
from django.urls import path

from analog import views

urlpatterns=[
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('customers/<str:pk>/',views.customers,name='customer'),
    path('create_order/<str:pk>/',views.createOrder,name='create_order'),
    path('update_order/<str:pk>/',views.updateOrder,name='update_order'),
    path('delete_order/<str:pk>/',views.deleteOrder,name='delete_order'),
    path('register/',views.Register,name='register'),
    path('log_in/',views.LogIn,name='log_in'),
    path('log_out/',views.LogOut,name='log_out'),
    path('user/',views.UserPage,name='user_page'),
]