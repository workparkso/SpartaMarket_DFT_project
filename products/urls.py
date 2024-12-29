from django.urls import path
from . import views

urlpatterns = [
    path('', views.product, name='product'), # 상품 생성 및 목록
    path('<int:pk>/', views.update_product, name='update_product'), # 상품 수정 및 삭제
]