from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    # Show user information in admin panel
    list_display = ['username', 'first_name', 'last_name', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth', 'bio', 'photo', 'job', 'phone')}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Show user posts
    list_display = ['description', 'create']
    search_fields = ['description', 'tags']


admin.site.register(Contact)