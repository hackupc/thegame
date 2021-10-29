from django.contrib import admin
from django.contrib.admin import ModelAdmin

from challenge.forms import ChallengeAdminForm
from challenge.models import Challenge, ChallengeUser, ChallengeTroll, VoteReaction


class ChallengeAdmin(ModelAdmin):
    form = ChallengeAdminForm


admin.site.register(Challenge, admin_class=ChallengeAdmin)
admin.site.register(ChallengeUser)
admin.site.register(ChallengeTroll)
admin.site.register(VoteReaction)
