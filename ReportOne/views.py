""" ReportOne views """
#from django.http import HttpResponse
#from django.http import Http404
#from django.template import loader

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Choice, Question

class IndexView(generic.ListView):
    """ this is Index view class"""
    template_name = 'ReportOne/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #my_list=["LatestRelease","Updates","API","License","GitHubProject","OldVersion4.7",
        # "ICONS","Gallery","Cheatsheet","RequestsLeaderboard","RequestanIcon","SUPPORT",
        # "Troubleshooting","CommonQuestions","ReportaBug",
        # "GetHelp","COMPANY","Blog","Status","ContactUs"]
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """ this is DetailView class"""
    model = Question
    template_name = 'ReportOne/detail.html'


class ResultsView(generic.DetailView):
    """ this is ResultView class"""
    model = Question
    template_name = 'ReportOne/results.html'

def vote(request, question_id):
    """ this is vote finction """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'ReportOne/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('ReportOne:results', args=(question.id,)))
