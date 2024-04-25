from django.urls import path
from . import views
from django.conf.urls import handler404
from django.shortcuts import render 


# handler404 = 'app1.views.error404' 
urlpatterns = [
    path('',views.index,name='index'),
    path('base',views.base,name='base'),
    path('categories',views.product,name='categories'),
    path('aboutus',views.about,name='about_us'),
    path('signup',views.signup,name='signup'),
    path('contact_us',views.contact_page,name='contact-us'),
    path('product/<slug:slug>',views.product_details,name='product_detail'),
    
    
    #cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    
    #wishlist
    
    path('wishlist/wishlist_detail/', views.wishlist_detail, name='wishlist_detail'),
    path('wishlist/add-to-wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove-from-wishlist/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    
    #checkout
    
    path('checkout/',views.checkout,name='checkout'),
    
    #order
    path('order/',views.ur_order,name='order'),
    path('delete_order_item/<int:order_item_id>/', views.delete_order_item, name='delete_order_item'),
    
    path('success',views.success,name='success'),
    
    #error page
    # path('404',views.error404,name='404'),
    
]
