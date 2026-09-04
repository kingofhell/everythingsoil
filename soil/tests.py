from django.test import TestCase
from django.urls import reverse
from .models import Element

class PublicViewsTests(TestCase):
    def test_homepage_loads(self):
        response = self.client.get(reverse('soil:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'soil/home.html')

    def test_soil_detail_loads(self):
        response = self.client.get(reverse('soil:soil_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'soil/soil_detail.html')

    def test_panja_bootham_loads(self):
        response = self.client.get(reverse('soil:panja_bootham'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'soil/panja_bootham.html')

    def test_element_detail_loads_successfully(self):
        # Element 'earth' is seeded in 0002_populate_elements migration
        earth = Element.objects.get(key='earth')
        response = self.client.get(reverse('soil:element_detail', args=[earth.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'soil/element_detail.html')
        self.assertContains(response, 'Earth')

    def test_lingeswarar_loads(self):
        response = self.client.get(reverse('soil:lingeswarar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'soil/lingeswarar.html')

    def test_about_loads(self):
        response = self.client.get(reverse('soil:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'soil/about.html')
