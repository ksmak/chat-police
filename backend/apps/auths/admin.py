from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rest_framework.authtoken.admin import TokenAdmin

from .models import CustomUser

TokenAdmin.raw_id_fields = ["user"]


class CustomUserAdmin(UserAdmin):
    """CustomUser admin."""

    list_display = ("id", "username", "ip", "name", "is_active")

    list_display_links = ("id", "username", "ip", "name", "is_active")

    readonly_fields = ("id",)

    fieldsets = (
        (
            "Personal",
            {
                "classes": ("wide",),
                "fields": (
                    "id",
                    "username",
                    "ip",
                    "name",
                    "password",
                ),
            },
        ),
        (
            "Permissions",
            {
                "classes": ("wide",),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
    )

    add_fieldsets = (
        (
            "Personal",
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "ip",
                    "name",
                ),
            },
        ),
        (None, {"classes": ("wide",), "fields": ("password1", "password2")}),
    )

    search_fields = ("name",)
    ordering = ("name",)


admin.site.register(CustomUser, CustomUserAdmin)
