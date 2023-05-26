"""
Test for user API
"""

# from decimal import Decimal
# import datetime

# from django.utils import timezone, dateformat

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
import datetime

CREATE_USER_API = reverse("user:signup")
TOKEN_URL = reverse("token_obtain_pair")

def detail_url(user_id):
    return reverse('user:update-user', args=[user_id])

def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


def payloadWithConfirmPass(arg):

    payload = {
        'email': 'user@example.com',
        'first_name': 'Marko',
        'last_name': 'Markovic',        
        'password': arg,
        'confirm_password': arg,
    }
    return payload


def payloadUser(arg):
    payload = {
        'email': 'user@example.com',
        'first_name': 'Marko',
        'last_name': 'Markovic',        
        'password': arg,
    }
    return payload

class PublicUserApiTest(TestCase):
    """Test the public features of the userAPI"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self):
        """Test create user successfully"""
        data = payloadWithConfirmPass('test1234$$')
        res = self.client.post(CREATE_USER_API, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data['email'])


        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])        
        self.assertTrue(user.check_password(data['password']))       
        self.assertNotIn('password', res.data)

    def test_if_user_email_exist(self):
        """Test if user email exist"""

        data = payloadWithConfirmPass('test1234$$')
        create_user(**payloadUser("test1234$$"))

        res = self.client.post(CREATE_USER_API, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_password_to_short(self):
        """Test if password is less than 7 char"""
        data = payloadWithConfirmPass('test1')
        email = data["email"]
        res = self.client.post(CREATE_USER_API, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        getUser = get_user_model().objects.filter(
            email=email
        ).exists()

        self.assertFalse(getUser)

    def test_create_jwt_for_user(self):
        """Test for creating jwt for user"""

        payload = payloadUser("testpass123")
        create_user(**payload)
        dataToken = {
            "password": payload["password"],
            "email": payload["email"]
        }

        token = self.client.post(TOKEN_URL, dataToken)
        self.assertIn("access", token.data)
        self.assertEqual(token.status_code, status.HTTP_200_OK)

    def test_bad_credentials_for_jwt(self):
        """Test bad credentials for jwt"""
        payload = payloadUser("testpass123")
        create_user(**payload)
        dataToken = {
            "password": "jsjsjssjsjsjsj",
            "email": payload["email"]
        }

        token = self.client.post(TOKEN_URL, dataToken)
        self.assertNotIn("access", token.data)
        self.assertEqual(token.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test if no password to create token"""
        payload = payloadUser("testpass123")
        create_user(**payload)
        dataToken = {
            "password": "",
            "email": payload["email"]
        }

        token = self.client.post(TOKEN_URL, dataToken)
        self.assertNotIn("access", token.data)
        self.assertEqual(token.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """If user is not authorized"""

        res = self.client.get(detail_url(1), {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTest(TestCase):
    """test API request that require authentication."""

    def setUp(self) -> None:
        self.user = create_user(**payloadUser("test1234$$"))
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        """Test retriev profile success"""
        res = self.client.get(detail_url(1))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        date_joined_res = datetime.datetime.strptime(res.data["date_joined"], '%Y-%m-%dT%H:%M:%S.%fZ')
        date_j_r = date_joined_res.strftime('%Y-%m-%d %H:%M:%S')
        data_res = res.data
        data_res["date_joined"] = date_j_r
        date_joined = self.user.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(data_res, {
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "date_joined": date_joined
        })
    
    def test_post_method_not_allowed(self):
        """Test POST method not allowed for endpoint"""

        res = self.client.post(detail_url(1), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_first_name(self):
        """Test PATCH method for user"""

        update_data = {"first_name": "Momir", "password": "myNewPassword123"}

        res = self.client.patch(detail_url(1), update_data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data["first_name"])
        self.assertTrue(self.user.check_password(update_data["password"]))
        self.assertEqual(res.status_code, status.HTTP_200_OK)














