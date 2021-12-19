from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.


def index(request):
    ################################################################
    # pleum

    categories = Category.objects.all()
    blogs = Blogs.objects.all()
    lastest = Blogs.objects.all().order_by("-pk")[:4]
    # most views
    popular = Blogs.objects.all().order_by("-views")[:3]
    # least views
    suggestion = Blogs.objects.all().order_by("views")[:3]

    # pagination
    paginator = Paginator(blogs, 2)
    try:
        page = int(request.GET.get("page", "1"))
    except:
        page = 1

    try:
        blogPerpage = paginator.page(page)
    except (EmptyPage, InvalidPage):
        blogPerpage = paginator.page(paginator.num_pages)

    return render(
        request,
        "frontend/index.html",
        {
            "categories": categories,
            "blogs": blogPerpage,
            "lastest": lastest,
            "popular": popular,
            "suggestion": suggestion,
        },
    )


def blogDetail(request, id):
    singleBlog = Blogs.objects.get(id=id)
    singleBlog.views = singleBlog.views + 1
    singleBlog.save()
    categories = Category.objects.all()
    popular = Blogs.objects.all().order_by("-views")[:3]
    suggestion = Blogs.objects.all().order_by("views")[:3]
    return render(
        request,
        "frontend/blogDetail.html",
        {
            "blog": singleBlog,
            "popular": popular,
            "categories": categories,
            "suggestion": suggestion,
        },
    )


def searchCategory(request, cat_id):
    blogs = Blogs.objects.filter(category_id=cat_id)
    categories = Category.objects.all()
    popular = Blogs.objects.all().order_by("-views")[:3]
    suggestion = Blogs.objects.all().order_by("views")[:3]
    categoryName = Category.objects.get(id=cat_id)

    return render(
        request,
        "frontend/searchCategory.html",
        {
            "blogs": blogs,
            "popular": popular,
            "categories": categories,
            "suggestion": suggestion,
            "categoryName": categoryName,
        },
    )


def searchWriter(request, writer):
    blogs = Blogs.objects.filter(writer=writer)
    categories = Category.objects.all()
    popular = Blogs.objects.all().order_by("-views")[:3]
    suggestion = Blogs.objects.all().order_by("views")[:3]
    return render(
        request,
        "frontend/searchWriter.html",
        {
            "blogs": blogs,
            "popular": popular,
            "categories": categories,
            "suggestion": suggestion,
            "writer": writer,
        },
    )
