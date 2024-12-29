from django.urls import path
from . import views

app_name = 'accounts'


urlpatterns = [
    path('create/', views.create_user, name='create_user'), # 회원가입 create로

]