from django.db import models
from django.contrib.auth.models import User
from account.models import UserAccount

# Create your models here.
class BookCategory(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

class Book(models.Model):
    title= models.CharField(max_length=100)
    description= models.TextField()
    borrowing_price = models.IntegerField()
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to ='static/uploads/')

    def __str__(self):
        return self.title
    
    
class Borrower(models.Model):
    name= models.ForeignKey(UserAccount,on_delete= models.CASCADE)
    book= models.ForeignKey(Book,on_delete= models.CASCADE)
    borrowDate = models.DateTimeField(auto_now_add=True)
    balanceAfter = models.IntegerField(null=True, blank=True)

    def create(cls, name , book):
        obj = cls(name=name,book=book)
        return obj
    
    def __str__(self):
        return f'{self.name}:{self.book}'

class Review(models.Model):
    post = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=30)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return f"Review by {self.name}"