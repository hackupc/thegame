from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django_tables2 import SingleTableView

from challenge.forms import ChallengeTryForm
from challenge.mixins import ChallengePermissionMixin
from challenge.models import Challenge, ChallengeUser
from challenge.tables import ChallengeStatsTable
from user.mixins import IsStaffMixin


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'challenge_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenges = Challenge.objects.all().prefetch_related(
            Prefetch('challengeuser_set', queryset=ChallengeUser.objects.filter(user=self.request.user),
                     to_attr='player_try'))
        result = {}
        player = {}
        for challenge in challenges:
            try:
                aux2 = player.get(challenge.order, 0) + int(challenge.player_try[0].success)
                player[challenge.order] = aux2
            except IndexError:
                pass
            aux = result.get(challenge.order, [])
            aux.append(challenge)
            result[challenge.order] = aux
        max_challenge = sorted(player.items())[-1] or (1, 0)
        player_phase = max_challenge[0] + int(max_challenge[1] == len(result[max_challenge[0]]))
        context.update({
            'challenge_groups': result,
            'player_phase': player_phase,
        })
        return context


class ChallengeView(ChallengePermissionMixin, TemplateView):
    template_name = 'challenge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_id = kwargs.get('c_id')
        challenge = get_object_or_404(Challenge, pk=c_id)
        try:
            succeed = ChallengeUser.objects.get(user=self.request.user, challenge=challenge).success
        except ChallengeUser.DoesNotExist:
            succeed = False
        form = None if succeed else ChallengeTryForm()
        context.update({
            'challenge': challenge,
            'form': form
        })
        return context

    def post(self, request, **kwargs):
        form = ChallengeTryForm(request.POST)
        c_id = kwargs.get('c_id', 1)
        context = self.get_context_data(**kwargs)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            try:
                challenge_try = ChallengeUser.objects.get(user=self.request.user, challenge_id=c_id)
            except ChallengeUser.DoesNotExist:
                challenge_try = ChallengeUser(user=self.request.user, challenge_id=c_id)
            now = pytz.utc.localize(datetime.now())
            if challenge_try.attempt_date.tzinfo is None:
                challenge_try.attempt_date = pytz.utc.localize(challenge_try.attempt_date)
            challenge_try.attempts += 1
            if challenge_try.attempt_date < (now - timedelta(minutes=5)):
                challenge_try.attempt_date = now
                challenge_try.attempts = 1
            elif challenge_try.attempts > settings.ATTEMPTS_PER_5_MINUTES:
                form.add_error(None, 'Too many attempts! Only %s attempts per 5 minutes permitted' %
                               settings.ATTEMPTS_PER_5_MINUTES)
                context.update({'form': form})
                return render(request, template_name=self.template_name, context=context)
            challenge_try.total_attempts += 1
            if challenge_try.challenge.check_solution(code):
                challenge_try.success = True
                challenge_try.last_try = now
                challenge_try.save()
                return redirect('challenge-index')
            form.add_error('code', 'Invalid code')
            challenge_try.save()
        context.update({'form': form})
        return render(request, template_name=self.template_name, context=context)


class ChallengeStatsView(IsStaffMixin, SingleTableView):
    table_class = ChallengeStatsTable
    template_name = 'challenge_stats.html'

    def get_queryset(self):
        c_id = self.kwargs.get('c_id')
        return ChallengeUser.objects.filter(challenge_id=c_id).order_by('-success', 'last_try')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_id = self.kwargs.get('c_id')
        challenge = get_object_or_404(Challenge, pk=c_id)
        succeed = 0
        for c in context.get('object_list', []):
            succeed += int(c.success)
        context.update({'challenge': challenge, 'succeed': succeed})
        return context
