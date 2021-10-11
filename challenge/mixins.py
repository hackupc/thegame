from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404

from challenge.models import ChallengeUser


class ChallengePermissionMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        c_id = kwargs.get('id', 1)
        if c_id != 1:
            c_id -= 1
            try:
                if not ChallengeUser.objects.get(challenge_id=c_id, user=request.user).success:
                    return self.handle_no_permission()
            except ChallengeUser.DoesNotExist:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
