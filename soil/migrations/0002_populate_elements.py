from django.db import migrations
from django.utils.text import slugify

def populate_elements(apps, schema_editor):
    Element = apps.get_model('soil', 'Element')
    initial_elements = [
        ("earth", "Earth", "The foundation of all life. Soil is the living body of the earth.", 1),
        ("water", "Water", "The element of connection, flow, and cohesion. The blood of the landscape.", 2),
        ("fire", "Fire", "The element of transformation, energy, and warmth. Driving all metabolic systems.", 3),
        ("air", "Air", "The element of movement, breath, and exchange. Connecting all living creatures.", 4),
        ("space", "Space", "The container of all form. Giving freedom and potential to be.", 5),
    ]
    for key, name, desc, order in initial_elements:
        Element.objects.get_or_create(
            key=key,
            defaults={
                'name': name,
                'slug': slugify(name),
                'description': desc,
                'order': order,
                'is_active': True
            }
        )

def remove_elements(apps, schema_editor):
    Element = apps.get_model('soil', 'Element')
    Element.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('soil', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_elements, remove_elements),
    ]
