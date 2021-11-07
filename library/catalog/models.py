from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date

# Create your models here.


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=20, help_text="Enter a book genre: ")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    def __str__(self):
        return self.last_name

    def get_absolute_url(self):
        return reverse("author-detail", args=[(self.id)])


class Book(models.Model):
    STATUS = (
        ("Ruslan", "Rusel"),
        ("Albert", "Alb"),
    )
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book", related_name="Books"
    )
    summary = models.TextField(help_text="Print description for this book")
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )
    language = models.ManyToManyField(Language, help_text="Enter language")
    stat = models.CharField(max_length=200, choices=STATUS, default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])

    def display_genre(self):
        return ", ".join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = "Genre"


class BookInstance(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text='"Unique ID for this particular book across whole library"',
    )
    due_back = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=20)
    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )
    status = models.CharField(
        max_length=20,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        return f"{self.book} {self.id}"

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False
