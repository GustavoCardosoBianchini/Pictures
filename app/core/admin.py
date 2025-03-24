'''
django admin customization
'''

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models

class UserAdmin(BaseUserAdmin):
    '''Define the admin pages for users'''
    ordering = ['id']
    list_display = ['email', 'name']
    # fiedlsets precisam ser uma tupla não podem ser mutaveis
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Last_login'), {'fields': ('last_login',)}),
    )
    # impede que os campos sejam modificados
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

admin.site.register(models.ModelUser, UserAdmin)
admin.site.register(models.ModelPostagem)
