from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'patients', views.PatientViewSet, basename='patients')
router.register(r'counsellors', views.CounsellorViewSet, basename='counsellors')
router.register(r'appointments', views.AppointmentViewSet, basename='appointments')

urlpatterns = [
    path('api/', include(router.urls)),
    path('active_data/', views.ActiveDataOfAllView.as_view(), name='active_data'),
    path('appointments/active_appointments/', views.AppointmentViewSet.as_view({'get': 'active_appointments'}), name='active-appointments'),
    path('appointments/date_filter/', views.AppointmentViewSet.as_view({'get': 'date_filter'}), name='date-filter'),
]