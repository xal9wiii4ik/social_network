from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from apps.userprofile.models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Display custom user in admin panel"""

    list_display = ('username', 'email', 'is_staff',
                    'gender', 'phone', 'followers', 'subscribers')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'gender', 'phone', 'followers', 'subscribers')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
