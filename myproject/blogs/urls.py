from django.urls import path
from .views import index, blogDetail, searchCategory, searchName, searchWriter

urlpatterns = [
    path("", index),
    path("<int:id>", blogDetail, name="blogDetail"),
    path("category/<int:cat_id>", searchCategory, name="searchCategory"),
    path("writer/<str:writer>", searchWriter, name="searchWriter"),
    path("searchName", searchName, name="searchName"),
]
