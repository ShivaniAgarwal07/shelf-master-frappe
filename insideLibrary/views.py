from django.shortcuts import render, redirect
from .models import Book, Member, Transaction
from django.http import JsonResponse
import requests


# Create your views here.

# to view all books
def book_list(request): #request is HTTP request made by user (GET or POST)
    books= Book.objects.all() #selecting all the books to render in a table
    return render(request, 'books/book_list.html', {'books': books}) # in book_list.html template we will write how we want to display the fetched books into the UI.


# to add a new book
def add_book(request):
    if request.method== 'POST':
        title= request.POST['title']
        author= request.POST['author']
        isbn= request.POST['isbn']
        publisher= request.POST['publisher']
        num_pages= request.POST['num_pages']
        stock= request.POST['stock']
        Book.objects.create(title= title, author=author,isbn=isbn, publisher=publisher, num_pages=num_pages, stock=stock ) #we are creating an object with these fields
        return redirect('book_list')
    return render(request, 'books/add_book.html')

# to import books from API
def import_books(request):
    if request.method== 'POST':
        title= request.POST.get('title', '')
        page= request.POST.get('page', 1)
        response= requests.get(f'https://frappe.io/api/method/frappe-library?page={page}&title={title}')
        books= response.json().get('message', [])
        print(books)

        for book in books:
            Book.objects.get_or_create(
                title= book['title'],
                author= book['author'],
                isbn= book['isbn'],
                publisher= book['publisher'],
                num_pages= int(book['num_pages']),
            )

        return JsonResponse({'status': 'Books imported!'})
    return render(request, 'books/import_books.html')


