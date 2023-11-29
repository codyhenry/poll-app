import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

#execute using py manage.py test <app name> ex. polls

# Create your tests here.
class QuestionModelsTests(TestCase):
  def test_was_published_recently_with_future_question(self):
    #should return false for questions with pub_date in the future
    time = timezone.now() + datetime.timedelta(days=30)
    future_question = Question(pub_date=time)
    self.assertIs(future_question.was_published_recently(),False)
