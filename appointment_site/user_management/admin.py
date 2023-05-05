from django.contrib import admin

# Register your models here.
from .models import *

class UserAdmin(admin.ModelAdmin):
    fields = (
        "email",
        "first_name",
        "last_name",
        "password",
        "role",
        "is_superuser",
        "is_staff",
        "groups",
        "user_permissions",
        "date_joined",
        "can_view_report",
    )
    # list_display = (
    #     "id",
    #     "email",
    #     "role",
    #     "date_joined",
    #     "is_active",
    # )
    # search_fields = (
    #     "id",
    #     "email",
    #     "first_name",
    # )
    # ordering = (
    #     "-is_active",
    #     "email",
    # )
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
admin.site.register(Patient)
admin.site.register(Counsellor)
admin.site.register(Appointment)

