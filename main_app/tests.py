from django.test import Client, RequestFactory, TestCase

from .forms import MaintenanceForm
from .models import Plant, User
from .views import *

c = Client()

# Create your tests here.
class PlantTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="Test User", email="test123@email.com", password="top_secret"
        )

    def create_plant(self):
        return Plant.objects.create(
            name="Silver Satin Pothos",
            description="Dark leaves with silver spots; Resilient",
            light="Low",
            toxicity=1,
            environment="Indoor",
            watering_frequency=21,
            user=self.user,
        )

    def test_create_plant(self):
        plant = self.create_plant()
        
        self.assertEqual(len(Plant.objects.all()), 1)
        self.assertEqual(plant.name, "Silver Satin Pothos")
        self.assertEqual(plant.description, "Dark leaves with silver spots; Resilient")
        self.assertEqual(plant.light, "Low")
        self.assertEqual(plant.toxicity, 1)
        self.assertEqual(plant.environment, "Indoor")
        self.assertEqual(plant.watering_frequency, 21)
        self.assertEqual(plant.user.id, 1)
