from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# User Model admin panel
@admin.register(User)
class UserAdmin(UserAdmin):
    # Show user information in admin panel
    list_display = ['username', 'first_name', 'last_name', 'phone']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {'fields': ('date_of_birth', 'bio', 'photo', 'job', 'phone')}),
    )


# Post Model admin panel
def make_deactivation(modeladmin, request, queryset):
    # Deactivation selection posts
    result = queryset.update(active=False)
    modeladmin.message_user(request, f"{result} Post has been deactivated")
make_deactivation.short_description = "رد پست"

def make_activation(modeladmin, request, queryset):
    # Activation selection posts
    result = queryset.update(active=True)
    modeladmin.message_user(request, f"{result} Post has been activated")
make_activation.short_description = "نمایش پست"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Show user posts
    list_display = ['description', 'create']
    search_fields = ['description', 'tags']
    actions = [make_deactivation, make_activation]


# Contact Model admin panel
admin.site.register(Contact)