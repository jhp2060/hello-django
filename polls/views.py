from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice

class IndexView(generic.ListView):
    model = Question
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     ctx = {
#         'latest_question_list' : latest_question_list,
#     }
#     return render(request, 'polls/index.html', ctx)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # 미래의 질문에 접근 불가
        return Question.objects.filter(pub_date__lte=timezone.now())
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk = question_id)
#     ctx = {
#         'question': question,
#     }
#     return render(request, 'polls/detail.html', ctx)


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     ctx = {
#         'question' : question,
#     }
#     return render(request, 'polls/results.html', ctx)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        ctx = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', ctx)
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        # reverse is a function for returning url pattern from a view(polls:results)
        # with arguments(question.id)
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
