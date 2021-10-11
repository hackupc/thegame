from django.contrib import admin
from django.contrib.admin import ModelAdmin

from challenge.forms import ChallengeAdminForm
from challenge.models import Challenge, ChallengeUser


class ChallengeAdmin(ModelAdmin):
    form = ChallengeAdminForm


admin.site.register(Challenge, admin_class=ChallengeAdmin)
admin.site.register(ChallengeUser)
