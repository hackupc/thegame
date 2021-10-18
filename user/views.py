from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from user.forms import UsernameForm
from user.models import User


class ChooseUsername(LoginRequiredMixin, TemplateView):
    template_name = 'set_username.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'form': UsernameForm()})
        return context

    def post(self, request):
        form = UsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                User.objects.get(username=username)
                form.add_error('username', 'Username already chosen')
            except User.DoesNotExist:
                form.save()
                return redirect(reverse('home'))
        context = self.get_context_data()
        context.update({'form': form})
        return render(request, template_name=self.template_name, context=context)
