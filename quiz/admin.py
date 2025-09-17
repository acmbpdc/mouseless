from django.contrib import admin
from .models import Task, Card, Answer, Hint, SiteSetting
from markdownx.admin import MarkdownxModelAdmin
from adminsortable2.admin import SortableAdminMixin

@admin.register(Task)
class TaskAdmin(SortableAdminMixin, MarkdownxModelAdmin):
    list_display = ('name', 'question_type', 'points', 'correct', 'order')
    list_filter = ('question_type',)
    list_editable = ('points',)
    search_fields = ('name', 'text')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('question_type', 'order')
    
    fieldsets = (
        ('Question Details', {
            'fields': ('name', 'text', 'correct', 'points')
        }),
        ('Reference Document', {
            'fields': ('document',),
            'description': 'Upload a reference document that participants can download (PDF, Word, Excel, etc.)'
        }),
        ('Hint System', {
            'fields': ('hint', 'hint_points'),
            'description': 'Set up hints and their point cost'
        }),
        ('Challenge Type', {
            'fields': ('question_type',),
            'description': 'Choose whether this is a Mouseless or Keyboardless challenge'
        }),
    )


@admin.register(Card)
class CardAdmin(MarkdownxModelAdmin):
    fields = ('user', 'penalty_points', 'phase')
    list_display = ('user', 'phase', 'current_phase_score', 'mouseless_score', 'keyboardless_score', 'total_score', 'start', 'penalty_points')
    list_filter = ('phase',)
    readonly_fields = ('start', 'last_time')
    search_fields = ('user__username',)
    
    def current_phase_score(self, obj):
        return obj.current_phase_score
    current_phase_score.short_description = 'Current Phase Score'
    
    def total_score(self, obj):
        return obj.score
    total_score.short_description = 'Total Score'

@admin.register(Answer)
class AnswerAdmin(MarkdownxModelAdmin):
    fields = ('card', 'task', 'value')
    ordering = ('-time_submitted',)
    list_display = ('card', 'task', 'task_type', 'value', 'is_correct', 'time_submitted')
    list_filter = ('task__question_type', 'time_submitted')
    search_fields = ('card__user__username', 'task__name', 'value')
    
    def task_type(self, obj):
        return obj.task.question_type.title()
    task_type.short_description = 'Challenge Type'
    
    def is_correct(self, obj):
        return obj.value == obj.task.correct
    is_correct.boolean = True
    is_correct.short_description = 'Correct'
    
@admin.register(Hint)
class HintAdmin(MarkdownxModelAdmin):
    fields = ("user", "hint_task", "time_hint_taken")
    list_display = ("user", "hint_task", "task_type", "hint_cost", "time_hint_taken")
    list_filter = ('hint_task__question_type', 'time_hint_taken')
    search_fields = ('user__username', 'hint_task__name')
    
    def task_type(self, obj):
        return obj.hint_task.question_type.title()
    task_type.short_description = 'Challenge Type'
    
    def hint_cost(self, obj):
        return f"{obj.hint_task.hint_points} points"
    hint_cost.short_description = 'Cost'

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('current_phase_display', 'dark_mode')
    
    def current_phase_display(self, obj):
        phase = 'Keyboardless Phase (Dark Mode)' if obj.dark_mode else 'Mouseless Phase (Light Mode)'
        return phase
    current_phase_display.short_description = 'Current Challenge Phase'
    
    def has_add_permission(self, request):
        # Only allow one SiteSetting instance
        return not SiteSetting.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of SiteSetting
        return False
        
    fieldsets = (
        ('Challenge Phase Control', {
            'fields': ('dark_mode',),
            'description': '''
            <div style="background: #2c3e50; padding: 15px; border-radius: 5px; margin: 10px 0; color: #ecf0f1; border: 1px solid #34495e;">
                <h3 style="color: #3498db; margin-top: 0;">Phase Management</h3>
                <p><strong>Mouseless Phase (Light Mode OFF):</strong> Participants use only keyboard navigation</p>
                <p><strong>Keyboardless Phase (Dark Mode ON):</strong> Participants use only mouse navigation</p>
                <hr style="border-color: #34495e;">
                <p><em>⚠️ Switching phases will automatically update all participant progress and save their mouseless scores when moving to keyboardless phase.</em></p>
            </div>
            '''
        }),
    )

# Custom admin site configuration
admin.site.site_header = "Mouseless & Keyboardless Challenge Admin"
admin.site.site_title = "Challenge Admin Portal"
admin.site.index_title = "Challenge Administration Dashboard"