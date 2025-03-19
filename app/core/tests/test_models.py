"""
Tests for models
"""
from unittest.mock import patch
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelUserTest(TestCase):
    """tests for users"""

    def test_create_new_user(self):
        '''teste create a common user'''
        email = 'teste@example.com'
        password = 'pas123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_normalize_email(self):
        '''test normalize emails'''
        emails = [
            ['teste@EXample.com','teste@example.com'],
            ['Reste1@exampLE.com','Reste1@example.com'],
            ['TEst2@example.COM','TEst2@example.com']
        ]
        password = 'pas123'
        for email, expected in emails:
            user = get_user_model().objects.create_user(
                email=email,
                password=password
            )
            self.assertEqual(user.email, expected)


    def test_create_new_super_user(self):
        '''test create a super user'''
        email = 'teste@example.com'
        password = 'pas123'
        user = get_user_model().objects.create_super_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)



