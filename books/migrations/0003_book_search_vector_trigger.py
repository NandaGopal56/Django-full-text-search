from django.contrib.postgres.search import SearchVector
from django.db import migrations


def compute_search_vector(apps, schema_editor):
    Quote = apps.get_model("books", "Book")
    Quote.objects.update(search_vector=SearchVector("book_name", "description"))


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0002_book_search_vector_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TRIGGER search_vector_trigger
            BEFORE INSERT OR UPDATE OF book_name, description, search_vector
            ON books_book
            FOR EACH ROW EXECUTE PROCEDURE
            tsvector_update_trigger(
                search_vector, 'pg_catalog.english', book_name, description
            );
            UPDATE books_book SET search_vector = NULL;
            """,
            reverse_sql="""
            DROP TRIGGER IF EXISTS search_vector_trigger
            ON books_book;
            """,
        ),
        migrations.RunPython(
            compute_search_vector, reverse_code=migrations.RunPython.noop
        ),
    ]