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
