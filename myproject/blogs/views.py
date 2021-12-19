from django.shortcuts import render
from django.http import HttpResponse
from category.models import Category
from .models import Blogs, Queue, Stack
from django.core.paginator import Paginator, EmptyPage, InvalidPage

# Create your views here.


def index(request):
    categories = Category.objects.all()
    blogs = Blogs.objects.all()
    print(blogs[0].views)
    lastest = Blogs()
    popular = []
    lastest = []
    suggestion = []
    # บทความแนะนำ ใช้ Queue
    que = Queue()
    for i in blogs:
        que.add(i)
    mergeSort(que.data)  # ใช้ mergesort เรียงตามยอดview จาก น้อย->มาก
    for i in range(3):
        suggestion.append(que.pop())

    # บทความล่าสุด และ บทความยอดนิยม ใช้ stack
    stack = Stack()

    for i in blogs:
        stack.add(i)

    for i in range(2):
        lastest.append(stack.pop())

    quick_sort(
        0, stack.range() - 1, stack.data
    )  # ใช้ quicksort เรียงตามยอดview จาก น้อย->มาก

    for i in range(3):
        popular.append(stack.pop())

    # most views
    # popular = Blogs.objects.all().order_by('-views')[:3]
    # least views
    # suggestion = Blogs.objects.all().order_by('views')[:3]
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
    # singleBlog = Blogs.objects.get(id=id)
    blogs = Blogs.objects.all()
    singleBlog = binarySearch(
        blogs, 0, len(blogs) - 1, id
    )  # ใช้ binarysearch หาบทความที่มีid ตรงกัน
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
    # blogs = Blogs.objects.filter(category_id=cat_id)
    allblogs = Blogs.objects.all()
    blogs = []
    for i in allblogs:
        if i.category_id == cat_id:
            blogs.append(i)
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
    allBlogs = Blogs.objects.all()
    blogs = []
    print(allBlogs[0])
    for i in allBlogs:  # ใช้ linearsearch หาบทความตามชื่อผู้เขียน
        if i.writer == writer:
            blogs.append(i)
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


def insertionSort(arr):
    for i in range(1, len(arr)):

        key = arr[i]
        j = i - 1
        while j >= 0 and key.views > arr[j].views:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def mergeSort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2

        L = arr[:mid]

        R = arr[mid:]

        mergeSort(L)

        mergeSort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i].views < R[j].views:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1


def partition(start, end, array):

    pivot_index = start
    pivot = array[pivot_index]

    while start < end:

        while start < len(array) and array[start].views <= pivot.views:
            start += 1

        while array[end].views > pivot.views:
            end -= 1

        if start < end:
            array[start], array[end] = array[end], array[start]

    array[end], array[pivot_index] = array[pivot_index], array[end]

    return end


def quick_sort(start, end, array):

    if start < end:

        p = partition(start, end, array)

        quick_sort(start, p - 1, array)
        quick_sort(p + 1, end, array)


def binarySearch(arr, l, r, x):

    # Check base case
    if r >= l:

        mid = l + (r - l) // 2

        if arr[mid].id == x:
            return arr[mid]

        elif arr[mid].id > x:
            return binarySearch(arr, l, mid - 1, x)

        else:
            return binarySearch(arr, mid + 1, r, x)

    else:

        return -1
