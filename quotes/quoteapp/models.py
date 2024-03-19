from django.db.models import Model, CharField, ManyToManyField, ForeignKey, CASCADE

MAX_TAG_LENGTH = 50


class Tag(Model):
    name = CharField(max_length=MAX_TAG_LENGTH, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"


class Author(Model):
    fullname = CharField(max_length=150, null=False, unique=True)
    born_date = CharField(max_length=30, null=False)
    born_location = CharField(max_length=100, null=False)
    description = CharField(max_length=10000, null=False)

    def __str__(self):
        return f"{self.fullname}"

    def fullname_without_spaces(self):
        return self.fullname.replace(" ", "-")


class Quote(Model):
    tags = ManyToManyField(Tag)
    author = ForeignKey(Author, on_delete=CASCADE, default=None, null=True)
    quote = CharField(max_length=2000, null=False, unique=True)

    def __str__(self):
        return f"{self.quote[:15]}"


class TopTenTags(Model):
    name = CharField(max_length=MAX_TAG_LENGTH, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"
