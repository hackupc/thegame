from django.contrib import admin
from django.contrib.admin import ModelAdmin

from user.forms import UserAdminForm
from user.models import User


class UserAdmin(ModelAdmin):
    form = UserAdminForm


admin.site.register(User, admin_class=UserAdmin)
