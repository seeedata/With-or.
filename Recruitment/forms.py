from django import forms
from Recruitment.models import Question, Answer

''' 팀원 모집글 등록 폼 '''
class QuestionForm(forms.ModelForm):
    # 모델 폼은 Meta 클래스를 반드시 가져야 함
    class Meta:
        # 모델 폼과 연결된 모델
        model = Question
        # 사용할 모델의 필드
        fields = ['title', 'start_date', 'end_date', 'image', 'url', 'linkareer', 'category', 'num_people', 'comment']
        labels = {
            'title': '제목',
            'start_date': '공모전 시작일',
            'end_date': '공모전 마감일',
            'image': '공모전 이미지',
            'url': '공모전 사이트 링크',
            'linkareer': '링커리어 링크',
            'category': '카테고리',
            'num_people': '모집할 팀원 수',
            'comment': '짧은 한마디',
        }

''' 팀원 신청 폼 '''
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['comment']
        labels = {
            'comment': '짧은 한마디',
        }