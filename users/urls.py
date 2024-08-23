from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/<int:pk>/',  # pk: 사용자의 기본 키
         views.ProfileView.as_view(), name='profile'),  # 프로필 보기
    path('profile/modify/<int:pk>/',
         views.profile_modify, name='profile_modify'),  # 프로필 편집
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)