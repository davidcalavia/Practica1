from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, render_to_response
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from models import Author, Books, Genere, BooksReview
from forms import BooksForm


def mainpage(request):
    return render_to_response('base.html')

class BooksDetail(DetailView):
    model = Books
    template_name = 'books/books_detail.html'

    def get_context_data(self, **kwargs):
        context = super(BooksDetail, self).get_context_data(**kwargs)
        context['RATING_CHOICES'] = BooksReview.RATING_CHOICES
        return context

class BooksCreate(CreateView):
    model = Books
    template_name = 'booksList/form.html'
    form_class = BooksForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BooksCreate, self).form_valid(form)

def review(request, pk):
    books = get_object_or_404(Books, pk=pk)
    reviews = BooksReview(
        rating=request.POST['rating'],
        comment=request.POST['comment'],
        user=request.user,
        books=books)
    reviews.save()
    return HttpResponseRedirect(reverse('booksList:books_detail',
                                        args=(books.id,)))
