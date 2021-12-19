from django.contrib.auth import login
from django.shortcuts import redirect, render
from blogs.models import Blogs
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from category.models import Category
from django.core.files.storage import FileSystemStorage
from django.contrib import messages


@login_required(login_url="member")
def panel(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    countView = 0
    for blog in blogs:
        countView += blog.views
    print(countView)
    # countView = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    # from krs ^

    return render(request, "backend/index.html", {"blogs": blogs, "writer": writer, "blogCount": blogCount, "countView": countView})


@login_required(login_url="member")
def displayForm(request):
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    countView = 0
    for blog in blogs:
        countView += blog.views
    print(countView)
    # countView = Blogs.objects.filter(writer=writer).aggregate(Sum("views"))
    # from krs ^
    categories = Category.objects.all()

    return render(request, "backend/blogForm.html", {"blogs": blogs, "writer": writer, "blogCount": blogCount, "countView": countView, "categories": categories})


@login_required(login_url="member")
def insertData(request):
    try:
        if request.method == "POST" and request.FILES["image"]:
            datafile = request.FILES["image"]
            # get data from form
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]
            writer = auth.get_user(request)
            if str(datafile.content_type).startswith("image"):
                # upload
                fs = FileSystemStorage()
                img_url = "blogImages/"+datafile.name
                filename = fs.save(img_url, datafile)
                # save data
                blog = Blogs(name=name, category_id=category, description=description,
                             content=content, writer=writer, image=img_url)
                blog.save()
                messages.info(request, "save data successfully")
                return redirect("displayForm")
            else:
                messages.info(request, "please upload image file")
                return redirect("displayForm")
    except:
        return redirect("displayForm")


@login_required(login_url="member")
def deleteData(request, id):
    try:
        blog = Blogs.objects.get(id=id)
        fs = FileSystemStorage()
        # delete image local
        fs.delete(str(blog.image))
        # delete in db
        blog.delete()

        return redirect(panel)
    except:
        return redirect(panel)


@login_required(login_url="member")
def editData(request, id):
    blogEdit = Blogs.objects.get(id=id)
    writer = auth.get_user(request)
    blogs = Blogs.objects.filter(writer=writer)
    blogCount = blogs.count()
    countView = 0
    categories = Category.objects.all()
    for blog in blogs:
        countView += blog.views

    return render(request, "backend/editForm.html", {"blogEdit": blogEdit, "writer": writer, "blogCount": blogCount, "countView": countView, "categories": categories})


@login_required(login_url="member")
def updateData(request, id):
    try:
        if request.method == "POST":
            # pull before data
            blog = Blogs.objects.get(id=id)
            # get data from form
            name = request.POST["name"]
            category = request.POST["category"]
            description = request.POST["description"]
            content = request.POST["content"]

            # update data
            blog.name = name
            blog.category_id = category
            blog.description = description
            blog.content = content
            blog.save()
            # messages.info(request, 'update success')

            # update image
            if request.FILES["image"]:
                datafile = request.FILES["image"]
                if str(datafile.content_type).startswith("image"):
                    # delete image before
                    fs = FileSystemStorage()
                    fs.delete(str(blog.image))
                    # insert new image
                    img_url = "blogImages/"+datafile.name
                    filename = fs.save(img_url, datafile)
                    blog.image = img_url
                    blog.save()
                    return redirect('panel')
    except:
        return redirect('panel')
