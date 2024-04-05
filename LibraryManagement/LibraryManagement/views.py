from django.contrib import messages
from django.shortcuts import render, redirect
from books.models import BookCategory, Book, Borrower, Review
from account.models import UserAccount
from books.forms import ReviewForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, ListView
from django.views import View
from django.utils.decorators import method_decorator

def send_borrow_email(user, book, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'book' : book
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
        
# Create your views here.
class HomepageView(ListView):
    model = Book
    template_name = 'home.html'
    context_object_name = 'books'

    def get_queryset(self):
        brand_slug = self.kwargs.get('Brand_Slug')
        if brand_slug:
            bookcategory = BookCategory.objects.get(name=brand_slug)
            queryset = Book.objects.filter(category=bookcategory)
        else:
            queryset = Book.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.all()
        return context


def bookdetails(request,id):
    book_detail= Book.objects.get(id=id)
    bookreview=Review.objects.filter(post=book_detail)
  
    match = False
    if request.user.is_authenticated:
        account_instance = UserAccount.objects.get(user=request.user)
        borrower_instances = Borrower.objects.filter(name=account_instance)
        
        for borrower_instance in borrower_instances:
            if borrower_instance.book == book_detail:
                match = True
                break
        
    if request.method=='POST':
        form=ReviewForm(request.POST)
        if form.is_valid():
            newReview=form.save(commit=False)
            newReview.post=book_detail
            newReview.save()
    else:
         form=ReviewForm()
    return render(request,'bookdetails.html',{'form':form,'book':book_detail,'Reviews':bookreview,'match':match})


@method_decorator(login_required, name='dispatch')
class BorrowBookView(View):
    def get(self, request, id):
        book_detail = Book.objects.get(pk=id)
        account_instance = UserAccount.objects.get(user=request.user)
        
        if account_instance.balance >= book_detail.borrowing_price:
            account_instance.balance -= book_detail.borrowing_price
            account_instance.save()
            
            borrower_instance = Borrower(name=account_instance, book=book_detail, balanceAfter=account_instance.balance)
            borrower_instance.save()

            messages.success(request, f'Borrowed "{book_detail.title}" successfully')
            send_borrow_email(request.user, book_detail, "Borrowing Book Message", "BorrowBook_Email.html")
        else:
            messages.warning(request, 'You have less amount than the borrowing price!')

        return redirect('profile')


@method_decorator(login_required, name='dispatch')
class ReturnBookView(View):
    def get(self, request, id):
        book_detail = Book.objects.get(pk=id)
        account_instance = UserAccount.objects.get(user=request.user)
        borrower_instance = Borrower.objects.filter(name=account_instance, book=book_detail).first()

        if borrower_instance:
            borrower_instance.delete()

            account_instance.balance += book_detail.borrowing_price
            account_instance.save()
            messages.success(request, f'Successfully returned the book "{book_detail.title}"')
        return redirect('profile')