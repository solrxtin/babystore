from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.home, name='home'),
    path('department/<str:pk>/', views.department, name='department'),
    path('department/<str:pk>/add_item/', views.add_item, name='add_item'),
    path('all_items/', views.all_items, name='all_items'),
    path('item/<str:pk>/', views.item, name='item'),
    path('item/<str:pk>/update_item/', views.update_item, name='update_item'),
    path('item/<str:pk>/delete_item/', views.delete_item, name='delete_item'),
    path('item/<str:pk>/item_sales', views.item_sale, name='update_sale'),
    path('item/<str:pk>/item_multiple_sales', views.update_multiple_sales, name='update_multiple_sales'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('sales/', views.view_sales, name='view_sales'),
    path('sales/update/<str:x>/<str:y>/', views.update_quantity, name='update_quantity'),
    path('sales/add_sales/', views.add_sales, name='add_sales'),
    path('sales/add_multiple_sales/', views.add_multiple_sales, name='add_multiple_sales'),
    path('cart/', views.add_to_cart, name="cart"),
    path('cart/<str:pk>/', views.add_item_to_cart, name="item_cart"),
    path('cart/view_cart', views.view_cart, name="view_cart"),
    path('cart/view_cart/checkout', views.checkout, name="checkout"),
    path('cart/view_cart/checkout/print_receipt', views.print_receipt, name="print_receipt"),
    path('cart/view_cart/<str:pk>/update', views.update_cart, name="update_cart"),
    path('cart/view_cart/<str:pk>/delete', views.delete_cart, name="delete_cart"),
    ]