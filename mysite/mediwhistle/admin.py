from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserProfile, Document, Comment, Form

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'UserProfile'
    fields = ('is_site_admin',)  # Ensure 'is_site_admin' is editable

# Extend the default UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, )

    # This method is adjusted to include all users without excluding site admins
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    # Adjust get_form to not disable fields for non-superusers
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    # Optionally, adjust list_display to include 'is_site_admin' status
    list_display = BaseUserAdmin.list_display + ('is_site_admin_status',)

    def is_site_admin_status(self, obj):
        return obj.userprofile.is_site_admin
    is_site_admin_status.boolean = True
    is_site_admin_status.short_description = 'Is Site Admin?'

# Unregister the original User admin and then register the modified UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register Document and Comment models
admin.site.register(Document)
admin.site.register(Form)
admin.site.register(Comment)
