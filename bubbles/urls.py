from django.urls import path
from bubbles import views

urlpatterns = [

    path('bubble/list', views.bubble_list_handle),
    path('bubble/detail', views.bubble_detail_handle),
    path('login', views.login_handle),
    path('bubble/publish', views.bubble_upload_handle)

]