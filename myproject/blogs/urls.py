from django.urls import path
from .views import index, blogDetail, searchCategory, searchName, searchWriter

urlpatterns = [
    path("", index),
    path("blog/<int:id>", blogDetail, name="blogDetail"),
    path("blog/category/<int:cat_id>", searchCategory, name="searchCategory"),
    path("blog/writer/<str:writer>", searchWriter, name="searchWriter"),
    path("searchName", searchName, name="searchName"),
]
