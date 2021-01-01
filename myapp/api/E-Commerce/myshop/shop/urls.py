from django.urls import path,include
from shop import views

app_name='shop'

urlpatterns = [

           path('product/<int:pk>/',views.ProductDetailView.as_view(),name='detail'),
           path('cart/<int:pk>',views.Add_To_Cart,name='add_to_cart'),
           path('cart/',views.cart,name='cart'),
           path('cart/delete/<int:pk>',views.delete_from_cart,name='delete_from_cart'),
           path('cart/delete_entire/<int:pk>',views.delete_entire,name='delete'),
           path('cart/checkout',views.checkout,name='checkout'),
           #path('cart/c',views.changecart,name='ccart'),
           path('cart/checkout/address',views.AddressCreateView.as_view(),name='form'),
           path('final',views.finalview,name='final'),
           path('category/',views.CategoryListView.as_view(),name='category'),
           path('register/',views.UserCreateView.as_view(),name='register'),
           path('category/<str:cats>',views.CategoryView,name='catlist'),
           path('profile/',views.ProfileView,name='profile'),



]
