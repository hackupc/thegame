from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from challenge.forms import ChallengeTryForm
from challenge.mixins import ChallengePermissionMixin
from challenge.models import Challenge, ChallengeUser


class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        challenge = ChallengeUser.objects.filter(user=request.user).order_by('-challenge_id')
        next_id = 1
        try:
            next_id = challenge[0].challenge_id + int(challenge[0].success)
        except IndexError:
            pass
        return redirect(reverse('challenge', args=[next_id]))


class ChallengeView(ChallengePermissionMixin, TemplateView):
    template_name = 'challenge.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_id = kwargs.get('c_id')
        challenge = get_object_or_404(Challenge, order=c_id)
        context.update({
            'challenge': challenge,
            'form': ChallengeTryForm(),
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
                challenge_try.save()
                return redirect('home')
            form.add_error('code', 'Invalid code')
            challenge_try.save()
        context.update({'form': form})
        return render(request, template_name=self.template_name, context=context)
