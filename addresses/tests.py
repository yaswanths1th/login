from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Pincode, Address
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()

class AddressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        Pincode.objects.create(pincode="110001", district="New Delhi", state="Delhi", country="India")
        self.client = APIClient()

    def test_get_location_success(self):
        resp = self.client.get(reverse("address-location"), {"pincode": "110001"})
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data["success"])
        self.assertIn("country", resp.data["data"])

    def test_get_location_not_found(self):
        resp = self.client.get(reverse("address-location"), {"pincode": "000000"})
        self.assertEqual(resp.status_code, 404)

    def test_create_address_success(self):
        payload = {
            "user_id": self.user.id,
            "flat_no": "12A",
            "street": "MG Road",
            "landmark": "Near Mall",
            "area": "Central",
            "pincode": "110001"
        }
        resp = self.client.post(reverse("address-create"), payload, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertTrue(resp.data["success"])
        self.assertEqual(Address.objects.count(), 1)

    def test_create_address_validation_fail(self):
        payload = {
            "user_id": self.user.id,
            "flat_no": "###!!!",  # invalid houseNo
            "street": "MG Road",
            "area": "Central",
            "pincode": "110001"
        }
        resp = self.client.post(reverse("address-create"), payload, format='json')
        self.assertEqual(resp.status_code, 400)

