from django.db import models

# Create your models here.
class Book(models.Model):
    id = models.BigAutoField(primary_key=True, db_index=True, editable=False)
    book_name = models.CharField(max_length=50)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name