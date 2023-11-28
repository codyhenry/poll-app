from django.db import models

# Create your models here.
class Question(models.Model):
  question_text = models.CharField(max_length=200)
  pub_date = models.DateTimeField("date published") #column name is date published instead of pub_date

class Choice(models.Model):
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  choice_text = models.CharField(max_length=200)
  votes = models.IntegerField(default=0)


"""
Change models in models.py file
Run <py manage.py makemigrations> to create migrations for the changes
Run <py manage.py migrate> to apply the changes to the database
"""