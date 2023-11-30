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

  def test_was_published_recently_with_old_question(self):
    #should return false for questions with pub_date older than 1 day
    time = timezone.now() - datetime.timedelta(days=1,seconds=1)
    old_question = Question(pub_date=time)
    self.assertIs(old_question.was_published_recently(),False)

  def test_was_published_recently_with_recent_question(self):
    #should return true for questions with pub_date within 1 day
    time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
    recent_question = Question(pub_date=time)
    self.assertIs(recent_question.was_published_recently(),True)