from django.test import Client, RequestFactory, TestCase

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

    
