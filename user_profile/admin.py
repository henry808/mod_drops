from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from user_profile.models import UserProfile


class ProfileInLine(admin.TabularInline):
    model = UserProfile


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Info', {'fields': ['username', 'first_name', 'last_name', 'email', 'password']}),
        ('Status', {'fields': ['is_staff', 'is_active', 'is_superuser']}),
        ('Date Information', {'fields': ['date_joined', 'last_login']}),
        ('Permissions', {'fields': ['groups', 'user_permissions']}),
    ]

    readonly_fields = ('password', 'date_joined', 'last_login')
    inlines = [
        ProfileInLine
    ]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
