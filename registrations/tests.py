from django.test import TestCase
from .models import Registration

class SimpleTest(TestCase):
    def test_create_registration(self):
        r = Registration.objects.create(name="Jay", email="jay@gmail.com")
        self.assertEqual(r.name, "Jay")
 
