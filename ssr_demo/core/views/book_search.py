from django.http import HttpRequest
from django.shortcuts import render


def book_search_view(request: HttpRequest):
    return render(request, 'core/book_search.html', {})
