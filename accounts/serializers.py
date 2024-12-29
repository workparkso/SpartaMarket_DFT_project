from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])  # 검증.
    password2 = serializers.CharField(write_only=True, required=True)  # 확인이라, validators 필요x

    class Meta:
        model = User # User모델 
        fields = ['email', 'username', 'password', 'password2', 'name', 'nickname', 'birth_date', 'gender', 'bio', 'profile_image'] 


    def validate(self, data): # 입력값이 맞는지 검토토
        if data['password'] != data['password2']: # 비밀번호와 비밀번호 확인이 다를 경우
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        
        if User.objects.filter(email=data['email']).exists(): # 이메일이 이미 존재하는 경우(유일)
            raise serializers.ValidationError({"email": "이메일이 이미 존재합니다."})
        
        if User.objects.filter(username=data['username']).exists(): # 사용자 이름이 이미 존재하는 경우(유일)
            raise serializers.ValidationError({"username": "Username이 이미 존재합니다"})
        

        return data

    def create(self, validated_data):
        validated_data.pop('password2') # 확인용인 비밀번호2는 삭제 -> 특정 삭제는 pop함수
        user = User.objects.create_user(**validated_data) # 사용자 생성
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'nickname', 'birth_date', 'gender', 'bio', 'profile_image'] # 공개 필드