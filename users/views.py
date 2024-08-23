from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


''' URL에서 전달된 특정 User 객체를 가져와, 해당 객체의 세부 정보를 템플릿에 렌더링 '''
class ProfileView(LoginRequiredMixin, DetailView):
    context_object_name = 'profile_user'  # 템플릿에서 User 객체를 참조할 때 사용할 이름
    model = User
    template_name = 'users/profile.html'
    login_url = 'common:login'  # 로그인이 안 되었으면 로그인 페이지로 이동

''' 프로필 편집 '''
@login_required(login_url='common:login')
def profile_modify(request, pk):
    user = get_object_or_404(User, pk=pk)
    profile, created = Profile.objects.get_or_create(user=user)
    # 프로필 편집 화면에서 '저장하기' 클릭 > 데이터 수정
    if request.method == 'POST':
        # profile을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 ProfileForm을 생성
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.save()
            return redirect('users:profile', pk=pk)
    # 프로필에서 '프로필 편집' 클릭 > GET 방식 호출 > 프로필 편집 화면
    else:
        form = ProfileForm(instance=profile)
    context = {'form': form}
    return render(request, 'users/profile_form.html', context)