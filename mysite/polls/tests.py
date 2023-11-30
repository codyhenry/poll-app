import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

#execute using py manage.py test <app name> ex. polls

#creates test question with text and offset days from now
def create_question(question_text, days):
  time = timezone.now() + datetime.timedelta(days=days)
  return Question.objects.create(question_text=question_text, pub_date=time)

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

class QuestionIndexViewTests(TestCase):
  def test_no_questions(self):
    #message when no questions exist
    response = self.client.get(reverse("polls:index"))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "No polls are available")
    self.assertQuerySetEqual(response.context["latest_question_list"], [])

  def test_past_questions(self):
    #question with past date should be displayed
    question = create_question(question_text="Past question",days=-30)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

  def test_future_question(self):
    #question with future date should not be displayed
    create_question(question_text="Future question",days=30)
    response = self.client.get(reverse("polls:index"))
    self.assertContains(response, "No polls are available")
    self.assertQuerySetEqual(response.context["latest_question_list"],[])

  def test_future_and_past_question(self):
    #only show past questions even if future ones exist
    question = create_question(question_text="Past question",days=-30)
    create_question(question_text="Future question",days=30)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerySetEqual(response.context["latest_question_list"],[question],)

  def test_two_past_questions(self):
    #show all questions that are in the past
    question1 = create_question(question_text="Past question 1",days=-30)
    question2 = create_question(question_text="Past question 2", days=-5)
    response = self.client.get(reverse("polls:index"))
    self.assertQuerySetEqual(response.context["latest_question_list"],[question2, question1],)

class QuestionDetailView(TestCase):
  def test_future_question(self):
    #detail view of future question should return 404
    future_question = create_question(question_text="Future question",days=5)
    url=reverse("polls:detail",args=(future_question.id,))
    response=self.client.get(url)
    self.assertEqual(response.status_code,404)

  def test_past_question(self):
    #detail view of question with pub_date in the past should show question_text
    past_question = create_question(question_text="Past question",days=-5)
    url=reverse("polls:detail",args=(past_question.id,))
    response=self.client.get(url)
    self.assertContains(response,past_question.question_text)