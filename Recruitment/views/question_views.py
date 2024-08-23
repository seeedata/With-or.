from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import QuestionForm
from ..models import Question
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os
from django.db.models import Sum

''' 팀원 모집 글 올리기 '''
@login_required(login_url='common:login')
def question_create(request):
    # 질문 등록 화면에서 입력값 채우고 '저장하기' 버튼 클릭 > POST 방식 요청 > 데이터 저장
    if request.method == 'POST':
        if 'crawl' in request.POST:
            linkareer = request.POST.get('linkareer')
            crawled_data = crawling(linkareer)
            if crawled_data:  # 크롤링된 데이터가 있으면
                form = QuestionForm(initial={
                    'title': crawled_data['title'],
                    'start_date': crawled_data['start_date'],
                    'end_date': crawled_data['end_date'],
                    'url': crawled_data['url'],
                    'linkareer': linkareer,
                })
            else:
                # 화면에서 전달받은 데이터로 폼이 채워지도록 객체를 생성
                form = QuestionForm(request.POST, request.FILES)  # FILES로 이미지를 전달
        else:
            # 화면에서 전달받은 데이터로 폼이 채워지도록 객체를 생성
            form = QuestionForm(request.POST, request.FILES)  # FILES로 이미지를 전달
        if form.is_valid():
            question = form.save(commit=False)  # 임시 저장
            question.author = request.user
            question.create_date = timezone.now()
            question.save()  # 실제 저장
            return redirect('Recruitment:index')
    # 질문 목록 화면에서 '질문 등록하기' 버튼 클릭 > GET 방식 요청 > 질문 등록 화면
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'Recruitment/question_form.html', context)

''' 팀원 모집 글 수정 '''
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 로그인한 사용자와 수정하려는 글쓴이가 다르면 '수정권한이 없습니다' 출력
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('Recruitment:detail', question_id=question.id)
    # 질문 수정 화면에서 '저장하기' 클릭 > 데이터 수정
    if request.method == 'POST':
        # question을 기본값으로 하여 화면으로 전달받은 입력값들을 덮어써서 QuestionForm을 생성
        form = QuestionForm(request.POST, request.FILES, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('Recruitment:detail', question_id=question.id)
    # 질문 상세 화면에서 '수정' 클릭 > GET 방식 호출 > 질문 수정 화면
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'Recruitment/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('Recruitment:detail', question_id=question.id)
    question.delete()
    return redirect('Recruitment:index')

def crawling(linkareer):
    try:
        html = requests.get(linkareer)
        soup = BeautifulSoup(html.text, "html.parser")

        title = soup.select_one(".title").text.strip()
        start_date = soup.select_one("h3 > div > span:nth-child(2)").text.strip()
        end_date = soup.select_one("h3 > span:nth-child(3)").text.strip()
        url = soup.select_one("h3 > div > div > a").text
        image_url = soup.select_one("figure.card-image-figure > img.card-image")['src']
        time.sleep(1)

        # 날짜 문자열을 Python의 datetime 객체로 변환
        start_date = datetime.strptime(start_date, "%Y.%m.%d")
        end_date = datetime.strptime(end_date, "%Y.%m.%d")

        # 이미지 다운로드 및 저장
        image_name = None
        if image_url:
            response = requests.get(image_url)
            if response.status_code == 200:
                # 이미지 파일명을 고유하게 생성
                image_name = title + '.jpg'
                # 이미지 저장 경로 설정
                save_path = os.path.join('media/image_recruitment', image_name)
                # 디렉토리가 없으면 생성
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                # 파일 저장
                with open(save_path, 'wb') as f:
                    f.write(response.content)

        return {
            'title': title,
            'start_date': start_date,
            'end_date': end_date,
            'image_name': image_name,
            'url': url
        }

    except Exception as e:
        print(f"An error occurred while crawling: {e}")
        return None