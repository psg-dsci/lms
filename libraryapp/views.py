# library/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Borrow
from django.contrib.auth.models import User
from .forms import BookForm

def home(request):
    books = Book.objects.all()
    return render(request, 'home.html', {'books': books})

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.available_copies > 0:
        book.available_copies -= 1
        book.save()
        borrow = Borrow.objects.create(user=request.user, book=book)
        return redirect('home')
    return render(request, 'home.html', {'error': 'No copies available', 'books': Book.objects.all()})
