from django.contrib import admin
from .models import BookCategory, Book, Borrower, Review

# Register your models here.
admin.site.register(BookCategory)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(Borrower)