from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Member, Transaction
from django.http import JsonResponse
import requests
from .forms import MemberForm
from django.utils.timezone import now


# Create your views here.

#for Books

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
        print(title, page)
        response= requests.get(f'https://frappe.io/api/method/frappe-library?page={page}&title={title}')
        books= response.json().get('message', [])
        print(books)

        for book in books:
            Book.objects.get_or_create(
                title= book['title'],
                author= book['authors'],
                isbn= book['isbn'],
                publisher= book['publisher'],
                num_pages= int(book['  num_pages']),
            )

        return JsonResponse({'status': 'Books imported!'})
    return render(request, 'books/import_books.html')


#for Members

#to view all members

def member_list(request):
    members= Member.objects.all()
    return render(request, 'members/member_list.html', {'members': members})

#to add a new member

def add_member(request):
    if request.method=='POST': 
        form= MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('member_list')

    else: 
        form= MemberForm()
    return render(request, 'members/add_member.html', {'form': form})

# to edit a member

def edit_member(request, pk):
    member= get_object_or_404(Member, pk=pk)
    if request.method=='POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('member_list')
    else: 
        form = MemberForm(instance=member)
    return render(request, 'members/edit_member.html', {'form': form})

# to delete a member

def delete_member(request, pk):
    member= get_object_or_404(Member, pk=pk)
    if request.method=='POST':
        member.delete()
        return redirect('member_list')
    return render(request, 'members/delete_member.html', {'member': member})



#for transactions

#to list all transactions

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-issue_date')  # Order by most recent
    return render(request, 'transactions/transaction_list.html', {'transactions': transactions})

# to issue a book

def issue_book(request):
    if request.method == "POST":
        member_id = request.POST.get('member')
        book_id = request.POST.get('book')
        issue_date = request.POST.get('issue_date')

        # Get the selected member and book
        member = Member.objects.get(id=member_id)
        book = Book.objects.get(id=book_id)

        # Check if stock is available
        if book.stock > 0:
            # Reduce stock and create a transaction
            book.stock -= 1
            book.save()
            Transaction.objects.create(member=member, book=book, issue_date=issue_date)
            return redirect('transaction_list')
        else:
            return render(request, 'transactions/issue_book.html', {
                'error': 'This book is currently out of stock.',
                'members': Member.objects.all(),
                'books': Book.objects.all(),
                'today': now().date()
            })

    return render(request, 'transactions/issue_book.html', {
        'members': Member.objects.all(),
        'books': Book.objects.all(),
        'today': now().date()
    })

# to return a book 

def return_book(request):
    if request.method == "POST":
        transaction_id = request.POST.get('transaction')
        return_date = request.POST.get('return_date')

        # Get the transaction
        transaction = Transaction.objects.get(id=transaction_id)

        # Calculate fees if returned late
        days_late = (now().date() - transaction.issue_date).days - 14  # Assume 14-day borrow period
        late_fee = 0
        if days_late > 0:
            late_fee = days_late * 5  # Rs. 5 per day late fee

        transaction.return_date = return_date
        transaction.fees = late_fee
        transaction.save()

        # Update book stock
        book = transaction.book
        book.stock += 1
        book.save()

        return redirect('transaction_list')

    return render(request, 'transactions/return_book.html', {
        'transactions': Transaction.objects.filter(return_date__isnull=True),
        'today': now().date()
    })


