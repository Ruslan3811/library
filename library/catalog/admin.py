from django.contrib import admin
from .models import Book, Genre, Author, BookInstance, Language

# Register your models here.


class BookInline(admin.TabularInline):
    model = Book
    extra = 0


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "last_name", "first_name", "date_of_birth", "date_of_death")
    fields = ["first_name", "last_name", ("date_of_birth", "date_of_death")]
    inlines = [BookInline]


admin.site.register(Author, AuthorAdmin)


class BooksInstanceInline(admin.TabularInline):
    extra = 0
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "display_genre")
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ("status", "due_back")
    list_display = ("book", "status", "due_back", "id", "borrower")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "book",
                    "imprint",
                    "id",
                )
            },
        ),
        ("Availability", {"fields": ("status", "due_back", "borrower")}),
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


models = Language
admin.site.register(models)
