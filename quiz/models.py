from email.policy import default
from django.contrib.auth.models import User
from django.db import models
from django.db.models import F, Sum, Max
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from datetime import datetime

class Task(models.Model):
    QUESTION_TYPES = [
        ('mouseless', 'Mouseless Challenge'),
        ('keyboardless', 'Keyboardless Challenge'),
    ]

    name = models.CharField(max_length=256)
    text = MarkdownxField()
    points = models.IntegerField()
    correct = models.CharField(max_length=256)
    hint = models.CharField(max_length=1000, default='No hint!!')
    hint_points = models.IntegerField(default=0)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mouseless')
    document = models.FileField(upload_to='task_documents/', null=True, blank=True, help_text='Upload reference document for participants')
    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ['points', 'order']

    @property
    def formatted_markdown(self):
        return markdownify(self.text)

    @property
    def document_name(self):
        """Get just the filename from the document path"""
        if self.document:
            return self.document.name.split('/')[-1]
        return None

    def is_completed(self, user):
        return Answer.objects.filter(card__user=user, task=self, value=self.correct).exists()

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})


class Card(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True, auto_now=False)
    penalty_points = models.IntegerField(default=0)
    mouseless_score = models.IntegerField(default=0)  # Score from mouseless phase
    keyboardless_score = models.IntegerField(default=0)  # Score from keyboardless phase
    phase = models.CharField(max_length=20, choices=[('mouseless', 'Mouseless'), ('keyboardless', 'Keyboardless')], default='mouseless')

    @property
    def solved_questions(self):
        return self.answer_set.filter(value=F('task__correct')).count()

    @property
    def mouseless_solved_questions(self):
        return self.answer_set.filter(value=F('task__correct'), task__question_type='mouseless').count()

    @property
    def keyboardless_solved_questions(self):
        return self.answer_set.filter(value=F('task__correct'), task__question_type='keyboardless').count()

    @property
    def score(self):
        mouseless_score = self.answer_set.filter(value=F('task__correct'), task__question_type='mouseless').aggregate(score=Sum('task__points')).get('score') or 0
        keyboardless_score = self.answer_set.filter(value=F('task__correct'), task__question_type='keyboardless').aggregate(score=Sum('task__points')).get('score') or 0
        
        # Calculate total hint penalties from both phases
        total_hints = Hint.objects.filter(user=self.user).count()
        total_penalty = total_hints * 2  # 2 points penalty per hint
        
        total_score = mouseless_score + keyboardless_score - total_penalty
        return max(0, total_score)

    @property
    def current_phase_score(self):
        if self.phase == 'mouseless':
            score = self.answer_set.filter(value=F('task__correct'), task__question_type='mouseless').aggregate(score=Sum('task__points')).get('score') or 0
        else:
            score = self.answer_set.filter(value=F('task__correct'), task__question_type='keyboardless').aggregate(score=Sum('task__points')).get('score') or 0
        return max(0, score - self.penalty_points)

    def update_mouseless_score(self):
        """Update the saved mouseless score when switching to keyboardless phase"""
        score = self.answer_set.filter(value=F('task__correct'), task__question_type='mouseless').aggregate(score=Sum('task__points')).get('score') or 0
        # Subtract hint penalties for mouseless phase
        mouseless_hints = Hint.objects.filter(user=self.user, hint_task__question_type='mouseless').count()
        penalty = mouseless_hints * 2  # 2 points penalty per hint
        self.mouseless_score = max(0, score - penalty)  # Ensure score doesn't go below 0
        self.save()
        return self.mouseless_score

    def update_keyboardless_score(self):
        """Update the saved keyboardless score when challenge is complete"""
        score = self.answer_set.filter(value=F('task__correct'), task__question_type='keyboardless').aggregate(score=Sum('task__points')).get('score') or 0
        # Subtract hint penalties for keyboardless phase
        keyboardless_hints = Hint.objects.filter(user=self.user, hint_task__question_type='keyboardless').count()
        penalty = keyboardless_hints * 2  # 2 points penalty per hint
        self.keyboardless_score = max(0, score - penalty)  # Ensure score doesn't go below 0
        self.save()
        return self.keyboardless_score

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

class SiteSetting(models.Model):
    dark_mode = models.BooleanField(default=False, help_text="Enable dark mode for all users")

    def __str__(self):
        return f"Dark Mode: {'On' if self.dark_mode else 'Off'}"