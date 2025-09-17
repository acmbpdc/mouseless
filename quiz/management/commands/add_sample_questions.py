from django.core.management.base import BaseCommand
from quiz.models import Task

class Command(BaseCommand):
    help = 'Add sample questions for testing the mouseless and keyboardless challenge'

    def handle(self, *args, **options):
        # Sample Mouseless Questions
        mouseless_questions = [
            {
                'name': 'Basic Navigation',
                'text': 'Navigate to the "About" section of any website using only keyboard shortcuts. What is the keyboard shortcut to focus on the address bar in most browsers?',
                'points': 10,
                'correct': 'Ctrl+L',
                'hint': 'Think about Location or aLternatively, it\'s commonly used to go to the address bar.',
                'hint_points': 3,
                'question_type': 'mouseless',
                'order': 1
            },
            {
                'name': 'Text Selection',
                'text': 'Without using the mouse, select all text in a document. What is the keyboard shortcut?',
                'points': 15,
                'correct': 'Ctrl+A',
                'hint': 'It\'s the first letter of the alphabet and stands for "All".',
                'hint_points': 5,
                'question_type': 'mouseless',
                'order': 2
            },
            {
                'name': 'Window Management',
                'text': 'How do you switch between open windows using only the keyboard?',
                'points': 20,
                'correct': 'Alt+Tab',
                'hint': 'Think about alternating between applications using a common modifier key.',
                'hint_points': 7,
                'question_type': 'mouseless',
                'order': 3
            }
        ]

        # Sample Keyboardless Questions
        keyboardless_questions = [
            {
                'name': 'Copy Text Without Keyboard',
                'text': 'You need to copy the text "Hello World" from one application to another using only your mouse. Describe one method to do this without using Ctrl+C.',
                'points': 15,
                'correct': 'Right-click menu',
                'hint': 'Think about context menus that appear when you perform a specific mouse action.',
                'hint_points': 5,
                'question_type': 'keyboardless',
                'order': 1
            },
            {
                'name': 'Virtual Keyboard Access',
                'text': 'How do you access the on-screen keyboard in Windows using only your mouse?',
                'points': 20,
                'correct': 'Start Menu > Settings > Ease of Access > Keyboard',
                'hint': 'Look in the accessibility or ease of access settings.',
                'hint_points': 8,
                'question_type': 'keyboardless',
                'order': 2
            },
            {
                'name': 'Browser Navigation',
                'text': 'Navigate to a new website using only mouse clicks. What browser element do you click first?',
                'points': 10,
                'correct': 'Address bar',
                'hint': 'It\'s at the top of the browser and shows the current URL.',
                'hint_points': 3,
                'question_type': 'keyboardless',
                'order': 3
            }
        ]

        # Add mouseless questions
        for q_data in mouseless_questions:
            task, created = Task.objects.get_or_create(
                name=q_data['name'],
                defaults=q_data
            )
            if created:
                self.stdout.write(f'Created mouseless question: {task.name}')
            else:
                self.stdout.write(f'Question already exists: {task.name}')

        # Add keyboardless questions
        for q_data in keyboardless_questions:
            task, created = Task.objects.get_or_create(
                name=q_data['name'],
                defaults=q_data
            )
            if created:
                self.stdout.write(f'Created keyboardless question: {task.name}')
            else:
                self.stdout.write(f'Question already exists: {task.name}')

        self.stdout.write(
            self.style.SUCCESS('Successfully added sample questions!')
        )
