from django.urls import path
from .views import base_views, question_views, answer_views, vote_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Recruitment'

urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),  # 팀원 모집 메인 페이지로
    path('<int:question_id>/',
         base_views.detail, name='detail'),  # 공모전 상세 페이지로

    # question_views.py
    path('question/create/',
         question_views.question_create, name='question_create'),  # 팀원 모집글 등록 페이지로
    path('question/modify/<int:question_id>/',
         question_views.question_modify, name='question_modify'),  # 팀원 모집글 수정
    path('question/delete/<int:question_id>/',
         question_views.question_delete, name='question_delete'),  # 팀원 모집글 삭제

    # answer_views.py
    path('answer/create/<int:question_id>/',
         answer_views.answer_create, name='answer_create'),  # 팀원 신청 페이지로
    path('answer/delete/<int:answer_id>/',
         answer_views.answer_delete, name='answer_delete'),  # 팀원 신청 취소
    path('add_team/<int:answer_id>/',
         answer_views.add_team, name='add_team'),  # 답글 단 사람을 팀원에 추가
    path('noadd_team/<int:answer_id>/',
         answer_views.noadd_team, name='noadd_team'),  # 답글 단 사람을 팀원에서 제외

    # vote_views.py
    path('vote/question/<int:question_id>/',
         vote_views.vote_question, name='vote_question'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)