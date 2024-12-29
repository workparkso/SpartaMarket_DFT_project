from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response


User = get_user_model()


@api_view(['POST']) # 생성 -> POST 요청 ok
@authentication_classes([])  # []는 동일 내용, 인증 관련, 비활성화로
@permission_classes([])      # []는 동일 내용, 권한 관련, 비활성화로
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "계정을 성공적으로 만들었습니다!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #만약 에러가 발생

