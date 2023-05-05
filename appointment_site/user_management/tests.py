from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta
from .models import Appointment, Patient, Counsellor
from .models import User
from django.utils import timezone


class AppointmentTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            email='user1@example.com', password='password')
        self.user2 = User.objects.create_user(
            email='user2@example.com', password='password')
        self.patient1 = Patient.objects.create(user=self.user1)
        self.patient2 = Patient.objects.create(user=self.user2)
        self.counsellor1 = Counsellor.objects.create(user=self.user1)
        self.counsellor2 = Counsellor.objects.create(user=self.user2)
        naive_datetime1 = datetime.now() + timedelta(days=1)
        naive_datetime2 = datetime.now() + timedelta(days=2)
        
        self.appointment1 = Appointment.objects.create(
            patient=self.patient1, counsellor=self.counsellor1, appointment_date=timezone.make_aware(naive_datetime1, timezone.get_current_timezone()), is_active=True)
        self.appointment2 = Appointment.objects.create(
            patient=self.patient2, counsellor=self.counsellor2, appointment_date=timezone.make_aware(naive_datetime2, timezone.get_current_timezone()), is_active=False)

    def test_get_appointments_by_patient_id(self):
        url = reverse('appointments-list') + '?patient_id=' + str(self.patient1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.appointment1.id)

    def test_get_appointments_by_counsellor_id(self):
        url = reverse('appointments-list') + '?counsellor_id=' + str(self.counsellor1.id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.appointment1.id)

    def test_get_active_appointments(self):
        url = reverse('active-appointments')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.appointment1.id)

    def test_get_appointments_by_date_range(self):
        start_date = datetime.now().strftime('%Y-%m-%d')
        end_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        url = reverse('date-filter') + f'?start_date={start_date}&end_date={end_date}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.appointment1.id)

    def test_create_appointment(self):
        url = reverse('appointments-list')
        data = {
            'patient_id': self.patient1.id,
            'counsellor_id': self.counsellor1.id,
            'appointment_date': '2023-06-05T08:01:03Z',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
