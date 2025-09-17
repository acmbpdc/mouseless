from django.core.management.base import BaseCommand
from quiz.models import SiteSetting, Card

class Command(BaseCommand):
    help = 'Switch between mouseless and keyboardless phases'

    def add_arguments(self, parser):
        parser.add_argument(
            'phase',
            choices=['mouseless', 'keyboardless'],
            help='Phase to switch to (mouseless or keyboardless)'
        )

    def handle(self, *args, **options):
        phase = options['phase']
        dark_mode = phase == 'keyboardless'
        
        # Update site setting
        site_setting, created = SiteSetting.objects.get_or_create(defaults={'dark_mode': dark_mode})
        site_setting.dark_mode = dark_mode
        site_setting.save()
        
        # Update all user cards to new phase
        for card in Card.objects.all():
            if card.phase != phase:
                if phase == 'keyboardless':
                    # Save mouseless score when switching to keyboardless
                    card.update_mouseless_score()
                    card.penalty_points = 0  # Reset penalties for new phase
                card.phase = phase
                card.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully switched to {phase} phase!')
        )
        if phase == 'keyboardless':
            self.stdout.write('All mouseless scores have been saved and penalties reset.')
