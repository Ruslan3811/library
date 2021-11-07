from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
import datetime
from django.forms import ModelForm
from .models import Book


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Enter a date between now and 4 weeks(default 3)"
    )

    def clean_renewal_date(self):
        date = self.cleaned_data["renewal_date"]

        if date and date > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks"))
        elif date and date < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))
        return date


class CreateBookModelForm(ModelForm):
    def clean_title(self):
        data = self.cleaned_data["title"]
        return data

    def clean_author(self):
        data = self.cleaned_data["author"]
        return data

    def clean_summary(self):
        data = self.cleaned_data["summary"]
        return data

    def clean_isbn(self):
        data = self.cleaned_data["isbn"]
        return data

    def clean_language(self):
        data = self.cleaned_data["language"]
        return data

    def clean_genre(self):
        data = []
        for genry in self.cleaned_data["genre"]:
            data.append(genry)
        return data

    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "summary",
            "isbn",
            "genre",
            "language",
        ]
        help_texts = {
            "summary": _("Enter a brief description of the book"),
            "isbn": _("13 Character ISBN number"),
            "genre": _("Select a genry for this book"),
        }
