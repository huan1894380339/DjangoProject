from hashlib import new
from rest_framework.test import APITestCase
from app.models import CustomerUser
from app.utils import active

class UserApiTest(APITestCase):
    def setUp(self) -> None:

        self.user  = CustomerUser.objects.create(email = "user1@gmail.com", username = "user 1")
        self.user.set_password("123")
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_register_user(self):
        new_user = {
            "email": "user2@gmail.com",
            "username": "user2",
            "password": "123",
            "password2": "123"
        }
        response = self.client.post('/app/api/user/sign_up/', new_user)
        self.assertEqual(response.status_code, 201)
        user2 = CustomerUser.objects.filter(email="user2@gmail.com").first()
        self.assertFalse(user2.is_active)

    def test_register_check_2_password_not_match(self):
        new_user = {
            "email": "user2@gmail.com",
            "username": "user2",
            "password": "123",
            "password2": "1243"
        }
        response = self.client.post('/app/api/user/sign_up/', new_user)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(str(response.data['non_field_errors'][0]), "Password confirm not match!")

    def test_sign_in(self):
        data = {
            "email" : self.user.email,
            "password" : "123"

        }
        response = self.client.post('/app/api/user/sign_in/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['access'])
        self.assertIsNotNone(response.data['refresh'])


