from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from ssr_demo.core import views


urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),

    path('', RedirectView.as_view(pattern_name='chat')),
    path('register/', views.CreateUserView.as_view(), name='register'),

    path('chat/', views.chat_view, name='chat'),
    path('chat/list/', views.list_messages_view, name='list-messages'),
    path('chat/create/', views.create_message_view, name='create-message'),

    path('books/', views.book_search_view, name='books'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
