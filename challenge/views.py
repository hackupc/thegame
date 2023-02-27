from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch, Avg
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django_tables2 import SingleTableView

from challenge.forms import ChallengeTryForm, VoteForm
from challenge.mixins import ChallengePermissionMixin
from challenge.models import Challenge, ChallengeUser, VoteReaction
from challenge.tables import ChallengeStatsTable
from thegame.log_utils import save_attempt, get_attempts
from thegame.utils import finished
from user.mixins import IsStaffMixin
from user.models import User


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'challenge_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenges = Challenge.objects.all().order_by('order').prefetch_related(
            Prefetch('challengeuser_set', queryset=ChallengeUser.objects.filter(user=self.request.user, success=True),
                     to_attr='player_try'))
        result = {}
        player = {}
        for challenge in challenges:
            aux2 = player.get(challenge.topic, {'order': 1, 'done': 0, 'challenges': 0})
            try:
                aux2['done'] += int(challenge.player_try[-1].success)
                if aux2['order'] != challenge.order:
                    aux2['order'] = challenge.order
                    aux2['challenges'] = 0
            except IndexError:
                pass
            if aux2['order'] == challenge.order:
                aux2['challenges'] += 1
            player[challenge.topic] = aux2
            aux = result.get(challenge.topic, [])
            aux.append(challenge)
            result[challenge.topic] = aux
        player = {topic: item['order'] + int(item['done'] == item['challenges']) for topic, item in player.items()}
        context.update({
            'challenge_groups': result,
            'player_phase': player,
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
        if not succeed and finished():
            form.fields['code'].disabled = True
        context.update({
            'challenge': challenge,
            'form': form
        })
        return context

    def post(self, request, **kwargs):
        form = ChallengeTryForm(request.POST)
        c_id = kwargs.get('c_id', 1)
        context = self.get_context_data(**kwargs)
        if finished():
            form.add_error(None, 'Time is up!')
            form.fields['code'].disabled = True
        elif form.is_valid():
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
            challenge_try.last_try = now
            if challenge_try.challenge.check_solution(code, request.user.id):
                challenge_try.success = True
                challenge_try.save()
                return redirect(reverse('challenge-vote', args=[challenge_try.challenge_id]))
            troll = challenge_try.challenge.check_troll(code)
            if troll is not None:
                return redirect(troll)
            save_attempt(code, user_id=request.user.id, challenge_id=challenge_try.challenge_id)
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
        average_vote = ChallengeUser.objects.filter(vote__isnull=False).aggregate(average=Avg('vote')).get('average', 0)
        for c in context.get('object_list', []):
            succeed += int(c.success)
        context.update({'challenge': challenge, 'succeed': succeed, 'average_vote': average_vote or 0})
        return context


class ChallengeStatsAttemptView(IsStaffMixin, TemplateView):
    template_name = 'challenge_stats_attempts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u_id = self.kwargs.get('u_id', None)
        if u_id is None:
            user = None
        else:
            user = get_object_or_404(User, id=u_id)
        c_id = self.kwargs.get('c_id')
        challenge = get_object_or_404(Challenge, pk=c_id)
        attempts = get_attempts(challenge_id=c_id, user_id=u_id)
        context.update({'attempts': attempts, 'challenge': challenge, 'user': user})
        return context


class VoteChallengeView(LoginRequiredMixin, TemplateView):
    template_name = 'challenge_vote.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_id = self.kwargs.get('c_id')
        challenge_user = get_object_or_404(ChallengeUser, challenge_id=c_id, user_id=self.request.user.id, success=True)
        context.update({'challenge': challenge_user.challenge, 'form': VoteForm(instance=challenge_user),
                        'max_vote': [(x, str(x)) for x in range(1, 11)]})
        return context

    def post(self, request, **kwargs):
        c_id = kwargs.get('c_id')
        challenge_user = get_object_or_404(ChallengeUser, challenge_id=c_id, user_id=request.user.id, success=True)
        form = VoteForm(request.POST, instance=challenge_user)
        if form.is_valid():
            instance = form.save()
            reaction = VoteReaction.TYPE_HAPPY if instance.vote > 5 else VoteReaction.TYPE_SAD
            return redirect(reverse('challenge-reaction', args=[challenge_user.challenge_id, reaction]))
        context = self.get_context_data()
        context.update({'form': form})
        return render(request, self.template_name, context=context)


class VoteChallengeReactionView(LoginRequiredMixin, TemplateView):
    template_name = 'challenge_vote_reaction.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_id = self.kwargs.get('c_id')
        r_type = self.kwargs.get('r_type')
        get_object_or_404(ChallengeUser, challenge_id=c_id, user_id=self.request.user.id, success=True,
                          vote__isnull=False)
        try:
            reaction = VoteReaction.objects.get(challenge_id=c_id, type=r_type)
            context.update({'reaction': reaction})
        except VoteReaction.DoesNotExist:
            pass
        return context
