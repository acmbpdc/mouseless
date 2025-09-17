from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView
)
from .forms import UserRegisterForm, AnswerForm
from .models import Task, Card, Answer, Hint, SiteSetting
from django.views.generic.edit import FormMixin


@login_required
def home(request):
    user = request.user
    if user.is_superuser or user.player_set.count() > 0:
        return render(request, 'quiz/home.html')
    else:
        messages.warning(request, f'Please enter the player details before attempting the challenge')
        return redirect('player-list')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.save()
            messages.success(request, f'Account created successfully!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'quiz/register.html', {'form': form})

class TaskListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Task
    template_name = 'quiz/task_list.html'
    context_object_name = 'tasks'

    def test_func(self):
        check = self.request.user.is_superuser or self.request.user.player_set.count() > 0
        if not check:
            messages.warning(self.request, f'Please enter the player details before attempting the challenge')
        return check

    def handle_no_permission(self):
        return redirect('player-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #if not self.request.user.is_superuser:
        card, _ = Card.objects.get_or_create(user=self.request.user)

        # Get current mode from site settings
        site_setting = SiteSetting.objects.first()
        current_mode = 'keyboardless' if (site_setting and site_setting.dark_mode) else 'mouseless'

        # Update user's phase if it doesn't match current mode
        if card.phase != current_mode:
            if current_mode == 'keyboardless':
                # When switching to keyboardless, save mouseless score
                card.update_mouseless_score()
                card.penalty_points = 0  # Reset penalties for new phase
            card.phase = current_mode
            card.save()

        context['card'] = card
        context['current_phase'] = current_mode

        return context

    def get_queryset(self):
        # Get current mode from site settings
        site_setting = SiteSetting.objects.first()
        current_mode = 'keyboardless' if (site_setting and site_setting.dark_mode) else 'mouseless'

        # Only show tasks for the current phase
        tasks = Task.objects.filter(question_type=current_mode).order_by('points', 'order')
        for task in tasks:
            task.completed = task.is_completed(self.request.user)
        return tasks



class TaskDetailView(LoginRequiredMixin, UserPassesTestMixin, FormMixin, DetailView):
    model = Task
    form_class = AnswerForm

    def get_success_url(self):
        return reverse('task-detail', kwargs={'pk': self.object.id})

    def test_func(self):
        check = self.request.user.is_superuser or self.request.user.player_set.count() > 0
        if not check:
            messages.warning(self.request, f'Please enter the player details before attempting the challenge')
        return check

    def handle_no_permission(self):
        return redirect('player-list')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        card = self.request.user.card
        answer , _ = Answer.objects.get_or_create(card=card, task=self.object)
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def get_context_data(self, **kwargs):
        context = super(TaskDetailView, self).get_context_data(**kwargs)
        card = self.request.user.card
        answer , _ = Answer.objects.get_or_create(card=card, task=self.object)
        context['form'] = AnswerForm(instance=answer)
        return context

    def form_invalid(self, form):
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.save()
        return super(TaskDetailView, self).form_valid(form)

@login_required
def leaderboard(request):
    leaderboard = list(filter(lambda t: t.score > 0 and not t.user.is_superuser, Card.objects.all()))
    if len(leaderboard) > 0:
        leaderboard = sorted(leaderboard, key=lambda t: (-t.score, t.last_time))[:10]

    # Get current mode for context
    site_setting = SiteSetting.objects.first()
    current_mode = 'keyboardless' if (site_setting and site_setting.dark_mode) else 'mouseless'

    context = {
        'leaderboard': leaderboard,
        'current_mode': current_mode
    }

    return render(request, 'quiz/leaderboard.html', context=context)

@login_required(login_url='login')
def showHint(request, pk):
    task = Task.objects.get(id=pk)
    card = Card.objects.get(user=request.user)
    hint_check = Hint.objects.filter(user=request.user, hint_task=task).exists()

    # Use current phase score for hint validation
    current_score = card.current_phase_score

    if ((current_score < task.hint_points) and (not(hint_check))):
        context = {
            'required_points': task.hint_points,
            'current_score': current_score,
            'task_name': task.name
        }
        return render(request, 'quiz/no_hint.html', context)
    else:
        if hint_check:
            hint = task.hint
            return render(request, 'quiz/hint.html', {'hint': hint, 'task_name': task.name})
        hint = task.hint
        card.penalty_points += task.hint_points
        card.save()
        h = Hint(user=request.user, hint_task=task)
        h.save()
        return render(request, 'quiz/hint.html', {'hint': hint, 'task_name': task.name})

def get_dark_mode_setting():
    setting = SiteSetting.objects.first()
    return setting.dark_mode if setting else False

# Context processor to inject dark_mode_enabled into all templates
def dark_mode_context(request):
    return {'dark_mode_enabled': get_dark_mode_setting()}
