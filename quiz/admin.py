from django.contrib import admin
from .models import Task, Card, Answer, Hint
from markdownx.admin import MarkdownxModelAdmin

@admin.register(Task)
class TaskAdmin(MarkdownxModelAdmin):
    fields = ('name', 'text', 'points', 'correct','hint','hint_points')
    list_display = ('name', 'points', 'correct',)


@admin.register(Card)
class CardAdmin(MarkdownxModelAdmin):
    fields = ('user','penalty_points')
    list_display = ('user', 'score', 'start', 'last_time','penalty_points',)

@admin.register(Answer)
class AnswerAdmin(MarkdownxModelAdmin):
    fields = ('card', 'task', 'value')
    ordering = ('-time_submitted',)
    list_display = ('card', 'task', 'value','time_submitted')
    
@admin.register(Hint)
class HintAdmin(MarkdownxModelAdmin):
    fields = ("user", "hint_task", "time_hint_taken")
    list_display = ("user", "hint_task", "time_hint_taken")