from django.contrib import admin

# Register your models here.
from .models import *

class PatientAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "user__email",
        "user__name",
        "is_active"
    )
    # list_filter = (
    #     "role",
    #     "is_active",
    #     "is_staff",
    #     "is_superuser",
    #     "date_joined",
    #     "last_login",
    # )

class CounsellorAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "user__email",
        "user__name",
        "is_active"
    )
    # list_filter = (
    #     "role",
    #     "is_active",
    #     "is_staff",
    #     "is_superuser",
    #     "date_joined",
    #     "last_login",
    # )


class AppointmentAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "appointment_date",
        "is_active"
    )
    # list_filter = (
    #     "role",
    #     "is_active",
    #     "is_staff",
    #     "is_superuser",
    #     "date_joined",
    #     "last_login",
    # )
# Register your models here.
admin.site.register(User)
admin.site.register(Patient,PatientAdmin)
admin.site.register(Counsellor,CounsellorAdmin)
admin.site.register(Appointment,AppointmentAdmin)

