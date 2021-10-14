from django.shortcuts import get_object_or_404, render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.db.models.aggregates import Avg

from .models import Book

def index(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all().order_by('-rating', 'title')
    total = books.count()
    average_rating = books.aggregate(Avg("rating"))

    return render(request, "book_outlet/index.html", {
        "books": books,
        "total": total,
        "average_rating": average_rating['rating__avg']
    })

def book_detail(request: HttpRequest, slug: str) -> HttpResponse:
    book = get_object_or_404(Book, slug=slug)
    return render(request, "book_outlet/book_detail.html", { "book": book })