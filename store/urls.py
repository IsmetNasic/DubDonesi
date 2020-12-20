from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Leave as empty string for base url
    path('', views.homePage, name="homePage"),
    path('store/', views.store, name="store"),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='store/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='store/logout.html'), name='logout'),

    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),



]
