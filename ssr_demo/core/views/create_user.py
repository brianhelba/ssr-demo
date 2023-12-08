from django import forms
from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView


class CreateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']


class CreateUserView(UserPassesTestMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'core/create_user.html'
    success_url = reverse_lazy('chat')

    def test_func(self):
        # Only allow anonymous users
        return not self.request.user.is_authenticated

    def form_valid(self, form: CreateUserForm):
        user: User = form.instance
        user.set_unusable_password()

        # Save the user
        resp = super().form_valid(form)

        login(self.request, user)
        return resp
