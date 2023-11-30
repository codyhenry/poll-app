from django.urls import path

from . import views

# namespace for urls
""" old views not using generic views
urlpatterns = [
  #/polls
  path("", views.index, name="index"),
  #/polls/5/
  path("<int:question_id>/", views.detail, name="detail"),
  #/polls/5/results
  path("<int:question_id>/results", views.results, name="results"),
  #/polls/5/vote
  path("<int:question_id>/vote", views.vote, name="vote"),
]
"""

app_name = "polls"
#int:pk used because DetailView expects primary key value to be called "pk"
urlpatterns = [
  #/polls
  path("", views.IndexView.as_view(), name="index"),
  #/polls/5/
  path("<int:pk>/", views.DetailView.as_view(), name="detail"),
  #/polls/5/results
  path("<int:pk>/results", views.ResultsView.as_view(), name="results"),
  #/polls/5/vote
  path("<int:question_id>/vote", views.vote, name="vote"),
]
