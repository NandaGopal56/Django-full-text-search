from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer

# Create your views here.
@api_view(['GET'])
def search(request):
    query  = request.GET.get('query')

    books = Book.objects.filter(book_name__icontains=query)
    serializer = BookSerializer(books, many=True)
    
    data = {
        "Keyword": query,
        "results": serializer.data
    }
    return Response(data)