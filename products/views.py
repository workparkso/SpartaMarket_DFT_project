from .models import Product
from rest_framework import status
from django.shortcuts import render
from .serializers import ProductSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination

# Create your views here.

@api_view(['POST', 'GET']) 
def product(request):
    if request.method == 'POST': # POST 요청인 경우 새 상품 생성
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user) # 현재 로그인한 유저가 작성자 ㅇㅇㅇ
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET': # GET 요청인 경우 상품 목록 반환
        products = Product.objects.all().order_by("created_at") # 작성일로부터 모든 상품 조회
        paginator = PageNumberPagination() # 페이지네이션 생성
        paginator.page_size = 5 # 페이지당 상품 수
        page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(page, many=True) 
        return Response(serializer.data, status=status.HTTP_200_OK) # 상품 목록 반환





@api_view(['PUT', 'DELETE']) # PUT, DELETE 요청만 허용
def update_product(request, pk):

    product = get_object_or_404(Product, pk=pk) # 상품 조회

    if request.method == 'PUT': # PUT 요청인 경우 상품 수정

        if product.author != request.user and not request.user.is_superuser: # 작성자 또는 관리자가 아닌 경우 삭제 불가능
            return Response({"error": "You do not have permission to edit this product."}, status=status.HTTP_403_FORBIDDEN) 

        serializer = ProductSerializer(product, data=request.data, partial=True) # 부분 업데이트 허용

        if serializer.is_valid(): # 유효성 검사
            serializer.save() # 저장

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    if request.method == 'DELETE': # DELETE 요청인 경우 상품 삭제

        if product.author != request.user and not request.user.is_superuser: # 작성자 또는 관리자가 아닌경우 삭제 불가능
            return Response({"error": "You do not have permission to delete this product."}, status=status.HTTP_403_FORBIDDEN)
        
        product.delete() # 삭제
        return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)