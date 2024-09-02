from email.policy import default
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Sum, Max
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from datetime import datetime

class Task(models.Model):
    name = models.CharField(max_length=256)
    text = MarkdownxField()
    points = models.IntegerField()
    correct = models.CharField(max_length=256)
    hint = models.CharField(max_length=256, default='No hint!!')
    hint_points = models.IntegerField(default=0)
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['order']

    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

    def is_completed_by(self, user): 
        return Answer.objects.filter(card__user=user, task=self, value=self.correct).exists()


class Card(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True, auto_now=False)
    penalty_points = models.IntegerField(default=0)
    solved_questions = models.IntegerField(default=0) 

    @property
    def solved_questions(self):
        return self.answer_set.filter(value=F('task__correct')).count()
    
    @property
    def score(self):
        score = self.answer_set.filter(value=F('task__correct')).aggregate(score=Sum('task__points')).get('score')
        if score is None:
            score = 0
        score -= self.penalty_points
        return score

    @property
    def last_time(self):
        last_time = self.answer_set.filter(value=F('task__correct')).aggregate(last_time=Max('submit')).get('last_time')
        if last_time is None:
            return None
        
        return str(last_time - self.start)

class Answer(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    value = models.CharField(max_length=256)
    submit = models.DateTimeField(auto_now=True)
    time_submitted = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('card', 'task'),)
        
class Hint(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    hint_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="hint_task")
    time_hint_taken = models.DateTimeField(auto_now=True)