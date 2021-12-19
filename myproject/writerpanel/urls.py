from django.urls import path
from .views import deleteData, displayForm, editData, insertData, panel, updateData
urlpatterns = [
    path('', panel, name="panel"),
    path('displayForm', displayForm, name="displayForm"),
    path('insertData', insertData, name='insertData'),
    path('deleteData/<int:id>', deleteData, name="deleteData"),
    path('editData/<int:id>', editData, name='editData'),
    path('updateData/<int:id>', updateData, name='updateData')
]
