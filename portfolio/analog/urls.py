from django.urls import path
from django.contrib.auth import views as auth_views
from analog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk>/', views.customers, name='customer'),
    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order'),
    path('register/', views.Register, name='register'),
    path('log_in/', views.LogIn, name='log_in'),
    path('log_out/', views.LogOut, name='log_out'),
    path('user/', views.UserPage, name='user_page'),
    path('user_setting/', views.settingProfile, name='user_setting'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='analog/password_reset.html'), name='reset_password'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='analog/reset_form.html'),name='password_reset_confirm'),
    path('reset_password_done/',auth_views.PasswordResetDoneView.as_view(template_name='analog/email_sent.html'),name='password_reset_done'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='analog/reset_complete.html'),name='password_reset_complete'),

]
