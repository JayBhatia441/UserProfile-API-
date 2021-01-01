from django.urls import path
from myapp.api import views

app_name:'myapp'

urlpatterns = [

    path('generic/profile/',views.GenericAPIView.as_view()),
    path('generic/profile/<int:pk>/',views.GenericAPIView.as_view()),
    path('post/',views.post_list),
    path('post/<int:pk>',views.post_detail),

]
