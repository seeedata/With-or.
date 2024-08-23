from django import forms
from users.models import Profile
from django.contrib.auth.models import User

''' 유저 가입 정보 수정 '''
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

''' 유저 프로필 수정 '''
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'major1', 'major1', 'grade', 'age', 'github_url', 'blog_url', 'sns_url', 'club', 'activity',
                  'contest', 'intern', 'intro', 'user_image']
        labels = {
            'nickname': '닉네임',
            'major1': '본전공',
            'major2': '이중전공/복수전공/부전공',
            'grade': '학년',
            'age': '나이',
            'github_url': 'Github',
            'blog_url': 'Blog',
            'sns_url': 'SNS',
            'club': '동아리/학회',
            'activity': '대외활동',
            'contest': '공모전',
            'intern': '인턴/학부연구생',
            'intro': '소개',
            'user_image': '프로필 사진'
        }