from django.contrib import admin
from django.contrib.admin import ModelAdmin

from challenge.forms import ChallengeAdminForm
from challenge.models import Challenge, ChallengeUser, ChallengeTroll, VoteReaction, ChallengeTopic


class ChallengeTrollAdmin(admin.StackedInline):
    model = ChallengeTroll
    extra = 1


class VoteReactionAdmin(admin.StackedInline):
    model = VoteReaction
    extra = 1


class ChallengeAdmin(ModelAdmin):
    form = ChallengeAdminForm
    inlines = [ChallengeTrollAdmin, VoteReactionAdmin]


admin.site.register(ChallengeTopic)
admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ChallengeUser)
