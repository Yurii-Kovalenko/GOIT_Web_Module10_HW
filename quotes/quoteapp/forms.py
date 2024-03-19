from django.forms import ModelForm, CharField, TextInput

from .models import Tag, Author, Quote, MAX_TAG_LENGTH


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=MAX_TAG_LENGTH, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=5, max_length=150, required=True, widget=TextInput())
    born_date = CharField(min_length=10, max_length=30, required=True, widget=TextInput())
    born_location = CharField(min_length=5, max_length=100, required=True, widget=TextInput())
    description = CharField(min_length=10, max_length=10000, required=True, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    quote = CharField(min_length=5, max_length=2000, required=True, widget=TextInput())

    class Meta:
        model = Quote
        fields = ['quote']
        exclude = ['tags', 'authors']