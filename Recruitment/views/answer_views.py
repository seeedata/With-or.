from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Sum
from ..forms import AnswerForm
from ..models import Question, Answer

''' 팀원 신청 '''
@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('Recruitment:detail', question_id=question.id), answer.id))
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'Recruitment/question_detail.html', context)

''' 팀원 신청 취소 '''
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '취소권한이 없습니다')
    else:
        answer.delete()
    return redirect('Recruitment:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def add_team(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question
    if request.user == question.author:
        answer.isteam = 1
        answer.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'}, status=403)

@login_required(login_url='common:login')
def noadd_team(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    question = answer.question
    if request.user == question.author:
        answer.isteam = 0
        answer.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': '권한이 없습니다.'}, status=403)



