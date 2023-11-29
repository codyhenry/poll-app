from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question
# Create your views here.

"""
def index(request):
  latest_question_list = Question.objects.order_by("-pub_date")[:5]
  template = loader.get_template("polls/index.html")
  context = {
    "latest_question_list": latest_question_list,
  }
  return HttpResponse(template.render(context,request))
"""

"""old endpoint
#shortcut to load template
def index(request):
  latest_question_list = Question.objects.order_by("-pub_date")[:5]
  context = {"latest_question_list": latest_question_list}
  return render(request, "polls/index.html", context)
"""

"""
def detail(request,question_id):
  try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question does not exist")
  return render(request, "polls/detail.html", {"question": question})
  # return HttpResponse("You're looking at question %s." % question_id) 
"""

""" old endpoints
#substitute try except with get_object_or_404
def detail(request,question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, "polls/results.html", {"question": question})
"""

class IndexView(generic.ListView):
  #will default to <app name>/<model name>_list.html if not given template_name
  #ex. polls/question_list.html
  template_name = "polls/index.html"
  #will default to <model name>_list if not given context_object_name
  #ex. question_list
  context_object_name = "latest_question_list"

  def get_queryset(self):
    return Question.objects.order_by("-pub_date")[:5]
  
class DetailView(generic.DetailView):
  model = Question
  #will default to <app name>/<model name>_detail.html if not given template_name
  #ex. polls/question_detail.html
  template_name = "polls/detail.html"
  #context_object_name will default to question

class ResultsView(generic.DetailView):
  model = Question
  template_name = "polls/results.html"

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST["choice"])
  except(KeyError, Choice.DoesNotExist):
    return render(request, "polls/detail.html", {"question": question, "error_message":"You did not select a choice."})
  else:
    selected_choice.votes+=1
    selected_choice.save()
    # return HttpResponseRedirect to prevent data from being POST twice if user hits back button
    return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))

"""
Each new view must be wired into .urls file
"""
