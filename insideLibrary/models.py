from django.db import models
from datetime import date
# Create your models here.

class Book(models.Model):
    title= models.CharField(max_length=200)
    author= models.TextField(max_length=35)
    isbn= models.CharField(max_length=20, unique=True)
    publisher= models.TextField(max_length=50)
    num_pages= models.IntegerField()
    stock= models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Member(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField(max_length=100, unique=True)
    existing_debt= models.IntegerField( default=0)

    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    book= models.ForeignKey(Book, on_delete=models.CASCADE ) #it will delete the transaction related to book instance when book will be deleted. 
    member= models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date= models.DateField(auto_now_add=True) # it will set the field to the current date when the object is created.
    return_date= models.DateField(null=True, blank=True) # initially date will be null and field will be blank and no validation error will occur. 
    fee= models.IntegerField()

    def is_overdue(self):
        if self.return_date: #checks if return_date exists or not
            return date.today()> self.return_date #if current date is greater than return date, then transaction is overdue
        return False #otherwise it will return false


