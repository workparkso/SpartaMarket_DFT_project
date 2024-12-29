from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer, ProfileSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404


User = get_user_model()


@api_view(['POST']) # 생성 -> POST 요청 ok
@authentication_classes([])  # []는 동일 내용, 인증 관련, 비활성화로(무시)
@permission_classes([])      # []는 동일 내용, 권한 관련, 비활성화로(무시시)
def create_user(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "계정을 성공적으로 만들었습니다!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #만약 에러가 발생


@api_view(['POST'])
@authentication_classes([])      # 전역 인증 설정 무시
@permission_classes([])  # 전역 IsAuthenticated 설정 무시
def login(request):
    if request.method == 'POST':
    username = request.data.get('username') #조회
    password = request.data.get('password') #조회

        # 사용자 인증
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # JWT 토큰 생성
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'message': '로그인 성공'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        
@api_view(['POST'])
@authentication_classes([])      # 전역 인증 설정 무시
@permission_classes([])  # 전역 IsAuthenticated 설정 무시
def logout(request):
    print('---')
    try:
        refresh_token = request.data.get("refresh") #refresh 토큰 get
        print(refresh_token)
        token = RefreshToken(refresh_token)
        print(token)
        token.blacklist()
        print('---')
        return Response({"message": "로그아웃 성공"},status=status.HTTP_200_OK)
    except Exception:
        return Response({"error": "로그아웃 실패"}, 
                      status=status.HTTP_400_BAD_REQUEST)
        
# 성공적인 로그인 시 토큰을 발급하고, 실패 시 적절한 에러 메시지를 반환
 
 
 
 
 
 
 #  로그인 상태 필요. 검증으로, 로그인 한 사용자만 프로필 조회 가능
 
 @api_view(['GET']) 
def profile(request, username):
    user = request.user 
    
    if request.method == 'GET': # GET 요청인 경우 프로필 조회
        user = get_object_or_404(User, username=username)   
        try:
            serializer = ProfileSerializer(user)

        except User.DoesNotExist: # 사용자가 존재하지 않는 경우
            return Response({"error": "사용자가 존재하지 않습니다다"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.data, status=status.HTTP_200_OK)        