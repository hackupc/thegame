from datetime import datetime

import pytz
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from challenge.models import ChallengeUser, Challenge


class ChallengePermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.username is None:
            return redirect(reverse('index'))
        if request.user.is_staff:
            c_id = kwargs.get('c_id', 1)
            challenge = get_object_or_404(Challenge, pk=c_id)
            if pytz.utc.localize(datetime.now()) < challenge.activation_date:
                return self.handle_no_permission()
            if challenge.order != 1:
                c_order = challenge.order - 1
                success = ChallengeUser.objects.filter(challenge__order=c_order, user=request.user,
                                                       success=True, challenge__topic=challenge.topic).count()
                challenges = Challenge.objects.filter(order=c_order, topic=challenge.topic).count()
                if challenges > success:
                    return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
