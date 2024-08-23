from django.db import models
from django.contrib.auth.models import User

''' 질문 모델 '''
class Question(models.Model):
    title = models.CharField(max_length=50)  # 공모전 제목. 글자 수 제한.
    create_date = models.DateTimeField()  # 작성일자
    url = models.URLField(max_length=200)  # 공모전 url
    start_date = models.DateTimeField(null=True, blank=True)  # 공모전 시작일자
    end_date = models.DateTimeField()  # 공모전 종료일자
    image = models.ImageField(upload_to='image_recruitment', null=True, blank=True)  # 공모전 이미지
    linkareer = models.URLField(max_length=200, null=True, blank=True)  # 링커리어 url
    category = models.IntegerField()  # 공모전 카테고리. 정수값으로 입력
    num_people = models.IntegerField(default=1)  # 모집할 인원
    comment = models.CharField(max_length=100, null=True, blank=True)  # 짧은 한마디
    modify_date = models.DateTimeField(null=True, blank=True)
    # on_delete=models.CASCADE: 계정이 삭제되면 계정과 연결된 Question 모델 데이터를 모두 삭제
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_question')
    voter = models.ManyToManyField(User, related_name='voter_question')  # 관심 보인 유저


''' 답변 모델 '''
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 질문
    comment = models.CharField(max_length=100)  # 짧은 한마디
    create_date = models.DateTimeField()  # 작성일자
    isteam = models.IntegerField(default=0, null=True, blank=True)  # 팀원 여부
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_answer')

