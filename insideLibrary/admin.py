from django.contrib import admin
from .models import Book, Member, Transaction

# Register your models here.

admin.site.register(Book)
admin.site.register(Member)
admin.site.register(Transaction)


#customizing admin interface 

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'isbn', 'stock')  # Fields to display in the admin list view
    search_fields = ('title', 'authors')  # Add a search box for these fields
    list_filter = ('publisher',)  # Add filters for these fields


class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'existing_debt')
    search_fields = ('name', 'email')
    list_filter = ('existing_debt')


