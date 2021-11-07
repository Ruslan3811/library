from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView,
    LoanedBooksByUserListView,
    BorrowersListForLibrariers,
    renew_book_librarian,
    index,
    AuthorDelete,
    AuthorCreate,
    AuthorUpdate,
    BookCreate,
    BookUpdate,
    BookDelete,
)
from django.conf.urls import url

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^books/$", BookListView.as_view(), name="list-books"),
    url(r"^books/(?P<pk>\d+)$", BookDetailView.as_view(), name="book-detail"),
    url(r"^authors/$", AuthorListView.as_view(), name="list-authors"),
    url(r"^mybooks/$", LoanedBooksByUserListView.as_view(), name="list-borrowed-books"),
    url(
        r"^borrows/$",
        BorrowersListForLibrariers.as_view(),
        name="list-borrowers-for-libraries",
    ),
    url(
        r"^book/(?P<pk>[-\w]+)/renew/$",
        renew_book_librarian,
        name="renew-book-librarian",
    ),
    path(r"^books/(?P<pk>\d+)$", AuthorDetailView.as_view(), name="author-detail"),
]

urlpatterns += [
    url(r"^author/create/$", AuthorCreate.as_view(), name="author_create"),
    url(
        r"^author/(?P<pk>\d+)/update/$",
        AuthorUpdate.as_view(),
        name="author_update",
    ),
    url(
        r"^author/(?P<pk>\d+)/delete/$",
        AuthorDelete.as_view(),
        name="author_delete",
    ),
]

urlpatterns += [
    url(r"^book/create/$", BookCreate, name="book-create"),
    url(r"^book/(?P<pk>\d+)/delete/$", BookDelete.as_view(), name="book-delete"),
    url(r"^book/(?P<pk>\d+)/update/$", BookUpdate, name="book-update"),
]
