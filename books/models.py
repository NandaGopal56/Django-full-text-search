from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField

# Create your models here.
class Book(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True, editable=False)
    book_name = models.CharField(max_length=50)
    description = models.TextField()
    search_vector = SearchVectorField(null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = (GinIndex(fields=["search_vector"]),)

    def __str__(self):
        return f"{self.book_name} :: {self.description}"