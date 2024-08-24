from django.shortcuts import render, get_object_or_404
from ..models import Question
from django.core.paginator import Paginator
from django.db.models import F, Q, Count
import logging
logger = logging.getLogger('Recruitment')

''' 공모전 목록 출력 '''
def index(request):
    logger.info("INFO 레벨로 출력")

    # 입력 인자
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')  # 모집 여부
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬 기준

    # 질문 목록 기본 쿼리셋
    question_list = Question.objects.all()

    if category:
        if category == '1':
            question_list = question_list.filter(category=1)
        elif category == '2':
            question_list = question_list.filter(category=2)
        elif category == '3':
            question_list = question_list.filter(category=3)
        elif category == '4':
            question_list = question_list.filter(category=4)

    # 정렬
    if so == 'recommend':
        # annotate: 모델에 없는, num_voter 필드를 임시로 추가
        question_list = question_list.annotate(
            num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(
            num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = question_list.order_by('-create_date')

    # 모집 여부
    if status:
        question_list = question_list.annotate(
            remaining_people=F('num_people') - Count('answer', filter=Q(answer__isteam=1)))
        if status == 'ongoing':
            question_list = question_list.filter(remaining_people__gt=0)
        elif status == 'completed':
            question_list = question_list.filter(remaining_people__lte=0)
    else:
        question_list = question_list.annotate(
            remaining_people=F('num_people') - Count('answer', filter=Q(answer__isteam=1))
        )

    # 조회
    if kw:
        question_list = question_list.filter(
            # __icontains: 대소문자를 가리지 않고, 필드에 문자열이 포함되었는지 찾아줌
            Q(title__icontains=kw) |  # 제목 검색
            Q(comment__icontains=kw) |  # 짧은 한마디 검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이 검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이 검색
        ).distinct()

    # 페이징 처리
    paginator = Paginator(question_list, 9)  # 페이지당 9개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj,
               'page': page,
               'kw': kw,
               'so': so,
               'status': status,
               'category': category}
    return render(request, 'Recruitment/question_list.html', context)

''' 공모전 상세 내용 출력 '''
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'Recruitment/question_detail.html', context)