from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import Group
admin.site.unregister(Group)
#apps
from accounts.models import User
from accounts.forms import UserCreationForm, UserChangeForm
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form, change_form = UserCreationForm, UserChangeForm
    list_display = ('phone', 'username', 'email', 'is_active')
    list_filter = ('is_admin', 'is_email_verify',)
    fieldsets = (
        ('Authentication', {'fields': ('phone', 'username', 'email', 'password', 'is_email_verify')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser','is_admin',)},),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'image')},),
    )
    add_fieldsets = (
        None, dict({
            'class': ('wide',),
            'fields': ('phone', 'password1', 'password2')
        })
    )
    search_fields = 'phone',
    ordering = 'phone',
    filter_horizontal = []