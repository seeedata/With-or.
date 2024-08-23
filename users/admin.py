from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile

''' 장고 admin 페이지에서 Profile 모델을 User 모델과 함께 인라인으로 표시'''
class ProfileInline(admin.StackedInline):
    model = Profile  # 인라인에서 사용될 모델은 Profile
    can_delete = False  # 관리자가 인라인으로 표시된 프로필을 삭제할 수 없음

''' user 모델에 대한 관리자 인터페이스를 사용자 정의 '''
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)  # 사용자 관리 페이지에 Profile을 인라인으로 추가.
                                # 관리자가 사용자 정보를 편집할 때 사용자와 연결된 프로필 정보도 함께 편집 가능

# 기존의 User 모델의 등록을 해제
admin.site.unregister(User)
# User 모델을 CustomUserAdmin 클래스와 함께 다시 등록함.
admin.site.register(User, CustomUserAdmin)