from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Role

class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('username', 'email', 'CNIC', 'DOB', 'address', 'created_at')
    filter_horizontal = ('roles',)

admin.site.register(User, UserAdmin)
admin.site.register(Role)