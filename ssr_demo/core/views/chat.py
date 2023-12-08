from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from profanity_check import predict

from ssr_demo.core.models import Message


class CreateMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data['content']
        if predict([content])[0] == 1:
            raise ValidationError('Your message contains profanity.')
        return content


@login_required
def create_message_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    form = CreateMessageForm(
        data=request.POST,
    )
    if form.is_valid():
        form.instance.creator = request.user
        form.save()

        # Create a new blank form, for further submissions
        form = CreateMessageForm()

    return render(
        request,
        'core/chat_create_message.html',
        {
            'form': form,
        }
    )


def _get_messages():
    limit = 50
    # Run the query with descending sorting, limit to the first results, then step in reverse
    return Message.objects.select_related('creator').order_by('-created')[:limit:-1]


def list_messages_view(request: HttpRequest):
    return render(
        request,
        'core/chat_list_messages.html',
        {
            'messages': _get_messages(),
        }
    )


def chat_view(request: HttpRequest):
    return render(
        request,
        'core/chat.html',
        {
            'form': CreateMessageForm(),
            'messages': _get_messages(),
        }
    )
