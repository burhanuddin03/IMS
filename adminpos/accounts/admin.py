from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.utils.translation import gettext as _

# Register your models here.
class UserAdmin(BaseUserAdmin):
    ordering=['id']
    list_display =['username','email','first_name','last_name','is_staff']
    fieldsets=(
        (
            None,
            {'fields':('username','password')}
        ),
        (
            _('Personal Info'),
            {'fields':('first_name','last_name','email','profile_pic')}
        ),
        (
            _('Permissions'),
            {'fields':('is_active','is_staff','is_superuser','is_admin','groups','user_permissions')}
        ),

        (
            _('Important dates'),
            {'fields':('last_login','date_joined')}
        )
    )

    add_fieldsets = (
        (
            None, 
            {"classes": ('wide',),
            'fields':('username','email','password1','password2','profile_pic')
            }
        ),
    )
    
admin.site.register(models.User,UserAdmin)