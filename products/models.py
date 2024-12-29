from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 작성자
    title = models.CharField(max_length=100)  # 제목
    content = models.TextField()  # 내용
    image = models.ImageField(upload_to='product_images/' , blank=False, null=False)  # 이미지(필수라서 false)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성일
    updated_at = models.DateTimeField(auto_now=True)  # 수정일

    def __str__(self):
        return self.title