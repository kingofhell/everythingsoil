from django.db import migrations
from django.utils.text import slugify

def populate_interests(apps, schema_editor):
    Interest = apps.get_model('accounts', 'Interest')
    initial_interests = [
        ("Soil", "🌱"),
        ("Natural Farming", "🚜"),
        ("Meditation", "🧘"),
        ("Yoga", "🕉️"),
        ("Nature", "🌳"),
        ("Water", "💧"),
        ("Fire", "🔥"),
        ("Air", "💨"),
        ("Space", "🌌"),
        ("Traditional Knowledge", "📜"),
        ("Volunteering", "🤝"),
        ("Research", "🔬"),
    ]
    for name, icon in initial_interests:
        Interest.objects.get_or_create(
            name=name,
            defaults={
                'slug': slugify(name),
                'icon': icon,
                'description': f"Interests related to {name}."
            }
        )

def remove_interests(apps, schema_editor):
    Interest = apps.get_model('accounts', 'Interest')
    Interest.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_interests, remove_interests),
    ]
