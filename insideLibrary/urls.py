from django.urls import path
from . import views

urlpatterns=[
    path('books/', views.book_list, name= 'book_list'),
    path('books/add/', views.add_book, name='add_book' ),
    path('books/import/', views.import_books, name='import_books'),
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.add_member, name='add_member'),
    path('members/edit/<int:pk>/', views.edit_member, name='edit_member'),
    path('members/delete/<int:pk>/', views.delete_member, name='delete_member'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/issue/', views.issue_book, name='issue_book'),
    path('transactions/return/', views.return_book, name='return_book'),
]