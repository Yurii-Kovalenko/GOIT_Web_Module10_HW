from django.shortcuts import render, redirect

from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required

from .forms import TagForm, AuthorForm, QuoteForm

from .models import Tag, Author, Quote, TopTenTags

QUOTES_PER_PAGE = 10


@login_required
def add_tag(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quoteapp:tag_done")
        else:
            return render(request, "quoteapp/add_tag.html", {"form": form})

    return render(request, "quoteapp/add_tag.html", {"form": TagForm()})


@login_required
def tag_done(request):
    return render(request, "quoteapp/tag_done.html")


@login_required
def add_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to="quoteapp:author_done")
        else:
            return render(request, "quoteapp/add_author.html", {"form": form})

    return render(request, "quoteapp/add_author.html", {"form": AuthorForm()})


@login_required
def author_done(request):
    return render(request, "quoteapp/author_done.html")


@login_required
def add_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            choice_author = Author.objects.filter(
                fullname__in=request.POST.getlist("authors")
            )
            for author_one in choice_author.iterator():
                new_quote.author = Author.objects.get(fullname=author_one)
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist("tags"))
            for tag_one in choice_tags.iterator():
                new_quote.tags.add(tag_one)

            return redirect(to="quoteapp:quote_done")
        else:
            return render(
                request,
                "quoteapp/add_quote.html",
                {"tags": tags, "authors": authors, "form": form},
            )

    return render(
        request,
        "quoteapp/add_quote.html",
        {"tags": tags, "authors": authors, "form": QuoteForm()},
    )


def top_ten_tags() -> list[str]:
    result = []
    tag_dict = dict()
    quotes = Quote.objects.all()
    for quote in quotes:
        for tag in quote.tags.all():
            if tag in tag_dict:
                tag_dict[tag] += 1
            else:
                tag_dict[tag] = 1
    sorted_dict = sorted(tag_dict.items(), key=lambda x: x[1], reverse=True)
    count = 0
    for tag_info in sorted_dict:
        result.append(tag_info[0].name)
        count += 1
        if count == 10:
            break
    return result


@login_required
def quote_done(request):
    top_tags = TopTenTags.objects.all()
    for tag in top_tags:
        TopTenTags.objects.get(name=tag.name).delete()
    for new_tag in top_ten_tags():
        tag = TopTenTags(name=new_tag)
        tag.save()
    return render(request, "quoteapp/quote_done.html")


@login_required
def edit(request):
    return render(request, "quoteapp/edit.html")


def required(request):
    return render(request, "quoteapp/required.html")


def main(request, page=1):
    top_tags = TopTenTags.objects.all()
    quotes = Quote.objects.all()
    paginator = Paginator(list(quotes), QUOTES_PER_PAGE)
    quotes_on_page = paginator.page(page)
    return render(
        request, "quoteapp/index.html", {"quotes": quotes_on_page, "top_tags": top_tags}
    )


def tag(request, search_tag, page=1):
    eleven = 11
    top_tags = TopTenTags.objects.all()
    quotes = [
        quote
        for quote in Quote.objects.all()
        if search_tag in [new_tag.name for new_tag in quote.tags.all()]
    ]
    paginator_tag = Paginator(quotes, QUOTES_PER_PAGE)
    quotes_tag_on_page = paginator_tag.page(page)
    return render(
        request,
        "quoteapp/tag.html",
        {"quotes": quotes_tag_on_page, "search_tag": search_tag, "top_tags": top_tags},
    )


def author(request, search_author):
    fullname = search_author.replace("-", " ")
    author = Author.objects.get(fullname=fullname)
    return render(request, "quoteapp/author.html", {"author": author})
