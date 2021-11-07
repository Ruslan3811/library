from django.shortcuts import render
from django.views import generic
from .models import Author, Book, BookInstance, Genre
from django.db import connection, reset_queries
import time
import functools
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from .forms import RenewBookForm
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy
from .forms import CreateBookModelForm


def BookCreate(request):
    if request.method == "GET":
        form = CreateBookModelForm()
    elif request.method == "POST":
        form = CreateBookModelForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, "catalog/book_form.html", {"form": form})


class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy("list-books")


def BookUpdate(request, pk):
    book_obj = get_object_or_404(Book, pk=pk)
    if request.method == "GET":
        form = CreateBookModelForm()
    elif request.method == "POST":
        form = CreateBookModelForm(request.POST)
        if form.is_valid():
            book_obj.title = form.cleaned_data["title"]
            book_obj.author = form.cleaned_data["author"]
            book_obj.isbn = form.cleaned_data["isbn"]
            book_obj.genre.set(form.cleaned_data["genre"])
            book_obj.language.set(form.cleaned_data["language"])
            book_obj.save()
    return render(request, "catalog/book_form_update.html", {"form": form})


class AuthorCreate(PermissionRequiredMixin, CreateView):
    permission_required = "catalog.can_marked_returned"
    model = Author
    fields = "__all__"
    initial = {
        "date_of_death": "12/10/2016",
    }


class AuthorUpdate(UpdateView):
    model = Author
    fields = ["first_name", "last_name", "date_of_birth", "date_of_death"]


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy("list-authors")


@permission_required("catalog.can_marked_returned")
def renew_book_librarian(request, pk):
    # ищем объект BookInstance с идентификатором pk
    BookInst = get_object_or_404(BookInstance, pk=pk)
    if request.method == "POST":
        # заполняем данными, которые были переданы с помощью запроса
        form = RenewBookForm(request.POST)
        if form.is_valid():
            BookInst.due_back = form.cleaned_data["renewal_date"]
            BookInst.save()
            return HttpResponseRedirect(reverse("list-borrowers-for-libraries"))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(
            initial={
                "renewal_date": proposed_renewal_date,
            }
        )
    return render(
        request, "book_renew_librarian.html", {"form": form, "bookinst": BookInst}
    )


class BorrowersListForLibrariers(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    paginate_by = 3
    template_name = "list_borrowed_users.html"

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact="o")


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "bookinstance_list_borrowed_user.html"
    paginate_by = 2

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact="o")
            .order_by("due_back")
        )


class AuthorDetailView(DetailView):
    model = Author
    template_name = "author_detail.html"


class AuthorListView(ListView):
    model = Author
    template_name = "author_list.html"
    paginate_by = 2


class BookDetailView(DetailView):
    model = Book
    template_name = "book_detail.html"


class BookListView(ListView):
    model = Book
    template_name = "book_list.html"
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["some_data"] = "Some data which was used"
        return context


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        # print(f"Function : {func.__name__}")
        # print(f"Number of Queries : {end_queries - start_queries}")
        # print(f"Finished in : {(end - start):.2f}s")
        return result

    return inner_func


@query_debugger
def index(request):
    s = SessionStore()
    s["last_login"] = 123
    s.create()
    s["first_login"] = 321
    s = SessionStore(session_key=s.session_key)
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_available_instances = BookInstance.objects.filter(status__exact="a").count()
    num_authors = Author.objects.all().count()
    num_genres = Genre.objects.all().count()
    num_genres_fantastic = Genre.objects.filter(name__icontains="fantastic").count()
    num_genres_thriller = Genre.objects.filter(name__icontains="thriller").count()
    num_genres_roman = Genre.objects.filter(name__icontains="roman").count()
    queryset = Book.objects.prefetch_related("genre")
    books = []
    for obj in queryset:
        genres = [genre.name for genre in obj.genre.all()]
        books.append(f"{obj}: {genres}")
    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1
    username = request.user
    return render(
        request,
        "index.html",
        context={
            "books_genres": books,
            "num_genres": num_genres,
            "num_genres_roman": num_genres_roman,
            "num_genres_thriller": num_genres_thriller,
            "num_genres_fantastic": num_genres_fantastic,
            "num_books": num_books,
            "num_instances": num_instances,
            "num_available_instances": num_available_instances,
            "num_authors": num_authors,
            "num_visits": num_visits,
            "username": username,
        },
    )


def send_email(request):
    subject = "Сброс пароля"
    html_message = render_to_string(
        "password_reset_email.html", {"email": settings.EMAIL_HOST_USER}
    )
    if request.method == "POST":
        email = request.POST.get("email")
        print("EMAIL:", email)
    plain_message = strip_tags(html_message)
    if subject and html_message and email:
        try:
            send_mail(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [email],
                html_message=html_message,
            )
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("../accounts/password_reset/done")
    else:
        return HttpResponse("Make sure all fields are entered and valid.")
