from django.db import models
from category.models import Category

# Create your models here.
class Blogs(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    # link Category from category
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )  # can't delete if stil have category
    writer = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to="blogImages", blank=True
    )  # blogImages is folder
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name  # เอาไปแสดงผลในหน้า admin


class Queue:
    def __init__(self):
        self.data = []

    def add(self, value):
        self.data.append(value)

    def pop(self):
        return self.data.pop(0)

    def range(self):
        return len(self.data)


class Stack:
    def __init__(self):
        self.data = []

    def add(self, value):
        self.data.append(value)

    def pop(self):
        return self.data.pop(-1)

    def range(self):
        return len(self.data)
