from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.views import APIView
from .models import Patient, Counsellor, Appointment, User
from datetime import datetime
from .serializers import *

class ActiveDataOfAllView(APIView):
    def get(self, request, format=None):
        active_patients = Patient.objects.filter(is_active=True)
        active_counsellors = Counsellor.objects.filter(is_active=True)
        active_appointments = Appointment.objects.filter(is_active=True)

        patient_serializer = PatientSerializer(active_patients, many=True)
        counsellor_serializer = CounsellorSerializer(active_counsellors, many=True)
        appointment_serializer = AppointmentSerializer(active_appointments, many=True)

        data = {
            "active_patients": patient_serializer.data,
            "active_counsellors": counsellor_serializer.data,
            "active_appointments": appointment_serializer.data,
        }

        return Response(data)


class AllAppointmentsView(generics.ListAPIView):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = AppointmentSerializer
    model = serializer_class.Meta.model

    def get_queryset(self):
        pass


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        patient = request.data.get('user')
        user_obj = User.objects.filter(email=patient["email"])
        if user_obj:
            data = request.data.copy()
            data['user_email'] = patient["email"]
            user = User.objects.get(email=patient["email"])
            serializer = ExistUserPatientSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def active_patient(self, request):
        # Get the start and end date range from query params
        

        # Filter appointments by date range and active status
        patient = Patient.objects.filter(is_active=True)

        # Serialize the queryset and return as response
        serializer = self.get_serializer(patient, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class CounsellorViewSet(viewsets.ModelViewSet):
    serializer_class = CounsellorSerializer
    queryset = Counsellor.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        patient = request.data.get('user')
        user_obj = User.objects.filter(email=patient["email"])
        if user_obj:
            data = request.data.copy()
            data['user_email'] = patient["email"]
            user = User.objects.get(email=patient["email"])
            serializer = ExistUserCounsellorSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            serializer.save(user=user)
        else:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def active_counsellor(self, request):
        # Get the start and end date range from query params
        

        # Filter appointments by date range and active status
        counsellor = Counsellor.objects.filter(is_active=True)

        # Serialize the queryset and return as response
        serializer = self.get_serializer(counsellor, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()

    def get_queryset(self):
        queryset = Appointment.objects.all()

        # get the patient or counsellor id from the request parameters
        patient_id = self.request.query_params.get('patient_id', None)
        counsellor_id = self.request.query_params.get('counsellor_id', None)

        # filter the queryset based on the patient or counsellor id
        if patient_id is not None:
            queryset = queryset.filter(patient_id=patient_id)
        elif counsellor_id is not None:
            queryset = queryset.filter(counsellor_id=counsellor_id)

        return queryset

    @action(detail=False, methods=['get'])
    def active_appointments(self, request):
        # Get the start and end date range from query params
        

        # Filter appointments by date range and active status
        appointments = Appointment.objects.filter(is_active=True)

        # Serialize the queryset and return as response
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def date_filter(self, request):
        # Get the start and end date range from query params
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        # Filter appointments by date range and active status
        appointments = Appointment.objects.filter(
            appointment_date__gte=datetime.strptime(start_date, "%Y-%m-%d"),
            appointment_date__lte=datetime.strptime(end_date, "%Y-%m-%d"),
            is_active=True
        ).order_by('-appointment_date')

        # Serialize the queryset and return as response
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        patient = request.data.get('patient_id')
        counsellor = request.data.get('counsellor_id')
        appointment_date = request.data.get('appointment_date')
        
        # check if patient and counsellor are active
        if not Patient.objects.filter(id=patient, is_active=True).exists():
            return Response({'error': 'Patient is not active'}, status=status.HTTP_400_BAD_REQUEST)
        if not Counsellor.objects.filter(id=counsellor, is_active=True).exists():
            return Response({'error': 'Counsellor is not active'}, status=status.HTTP_400_BAD_REQUEST)
        
        # check if patient or counsellor already has an appointment date range
        # if Appointment.objects.filter(patient=patient, is_active=True).exists() and \
        if datetime.strptime(appointment_date, "%Y-%m-%dT%H:%M:%S%z") <= Appointment.objects.filter(patient=patient).last().appointment_date:
            return Response({'error': 'Patient already has an active appointment'}, status=status.HTTP_400_BAD_REQUEST)
        # if Appointment.objects.filter(counsellor=counsellor, is_active=True).exists():
        if datetime.strptime(appointment_date, "%Y-%m-%dT%H:%M:%S%z") <= Appointment.objects.filter(counsellor=counsellor).last().appointment_date:
            return Response({'error': 'Counsellor already has an active appointment'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient_obj = Patient.objects.get(id=patient)
        counsellor_obj = Counsellor.objects.get(id=counsellor)
        serializer.save(patient=patient_obj,counsellor=counsellor_obj)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)




