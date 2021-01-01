from django.urls import path,include
from myapp import views

app_name='myapp'

urlpatterns = [

     path('create',views.ProfileCreateView.as_view(),name='create'),
     path('profile/<int:pk>/',views.ProfileDetailView.as_view(),name='detail'),
     path('profile/update/<int:pk>',views.ProfileUpdateView.as_view(),name='update'),
     path('create2',views.create_view,name='create2'),
     path('post/update/<int:id>',views.update_view,name='update2'),
     path('register',views.UserCreateView.as_view(),name='register'),
     path('post/delete/<int:id>',views.delete_view,name='update2'),
     


]
