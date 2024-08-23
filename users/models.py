from django.db import models
from django.conf import settings

''' 유저 프로필 '''
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 각 사용자마다 하나의 프로필
    nickname = models.CharField(max_length=8, null=True, blank=True)
    major1 = models.CharField(max_length=20, null=True, blank=True)
    major2 = models.CharField(max_length=20, null=True, blank=True)
    grade = models.IntegerField(null=True, blank=True)  # 학년: 정수로 입력
    age = models.IntegerField(null=True, blank=True)
    github_url = models.URLField(max_length=200, null=True, blank=True)  # github url
    blog_url = models.URLField(max_length=200, null=True, blank=True)
    sns_url = models.URLField(max_length=200, null=True, blank=True)
    club = models.TextField(null=True, blank=True)
    activity = models.TextField(null=True, blank=True)
    contest = models.TextField(null=True, blank=True)
    intern = models.TextField(null=True, blank=True)
    intro = models.TextField(null=True, blank=True)
    user_image = models.ImageField(upload_to='image_users', null=True, blank=True)