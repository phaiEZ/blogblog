from django.db import models
from django.db.models.fields import CharField

# Create your models here.
class Category(models.Model):
    name = CharField(max_length=255,unique=True)

    def __str__(self):
        return self.name