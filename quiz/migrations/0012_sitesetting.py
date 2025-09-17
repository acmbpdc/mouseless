from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0011_remove_card_solved_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dark_mode', models.BooleanField(default=False, help_text='Enable dark mode for all users')),
            ],
        ),
    ] 