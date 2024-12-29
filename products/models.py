from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinLengthValidator







# username과 이메일은 유일해야 하며 -> 즉 필수!!, 이메일 중복 검증(선택 기능)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields): # 생성
        if not username: # 사용자 이름이 없는 경우
            raise ValueError('username은 필수작성입니다')
        if not email: # 이메일이 없는 경우
            raise ValueError('email은 필수작성입니다')
        
        # 이메일 중복 검사 추가
        if self.model.objects.filter(email=email).exists():  
            raise ValueError('이 이메일은 이미 사용 중입니다.')

        
        
        email = self.normalize_email(email) # 이메일을 소문자로 변경해서 혼란방지, 통일
        user = self.model(username=username, email=email, **extra_fields) # 사용자 관련 생성
        user.set_password(password) # 비밀번호 설정
        user.save() #구현: 데이터 검증 후 저장?
        return user

# 관리자
    def create_superuser(self, username, email, password=None, **extra_fields): # 슈퍼유저 생성
        extra_fields.setdefault('is_staff', True) # 스태프 권한
        extra_fields.setdefault('is_superuser', True) # 슈퍼유저 권한 

        return self.create_user(username=username, email=email, password=password, **extra_fields) # 사용자 생성


# 조건 :  username, 비밀번호, 이메일, 이름, 닉네임, 생일 필수 입력하며 성별, 자기소개 생략 가능
class User(AbstractUser, PermissionsMixin): 
    #user은 이미 AbstractUser에서 정희되어서 다시 정의할 필요 없는게 맞나요?
   # 비밀번호
    email = models.EmailField(unique=True)  # 이메일 필드
    name = models.CharField(max_length=50)  # 이름 필드
    nickname = models.CharField(max_length=20)  # 닉네임 필드
    birth_date = models.DateField()  # 생년월일 필드
    gender = models.CharField(max_length=10, blank=True, null=True)  # 성별 필드(생략가능)
    bio = models.TextField(blank=True, null=True)  # 자기소개 필드(생략가능)
    
    
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)  # 프로필 이미지 필드, blank=True 인해 없어도 출력됨

    objects = CustomUserManager() #위에 매니저 정의해줬음으로, 그래서 회원가입할 때 user.objects로 접근 가능한 것이 이 때문

    USERNAME_FIELD = 'username'  # 로그인 시 이메일 사용하는 필드
    REQUIRED_FIELDS = ['email', 'name', 'nickname', 'birth_date']  # email은 자동으로 필수, 즉 필드 설정

    def __str__(self):
        return self.username