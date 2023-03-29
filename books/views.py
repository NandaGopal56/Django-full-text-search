from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


@api_view(['GET'])
def FullTextSearch(request):
    query  = request.GET.get('query')

    query = "|".join(query.split(' ')) #joining the space separated words with | for OR condition

    search_query = SearchQuery(query, search_type='raw', config='english')
    search_vector = SearchVector('book_name', weight='A', config='english') + SearchVector('description', weight='B')

    books = Book.objects.annotate(
        search=search_vector,
        rank=SearchRank(search_vector, search_query)
    ).filter(search=search_query).order_by("-rank")
    
    serializer = BookSerializer(books, many=True)
    
    data = {
        "Keyword": query,
        "results": serializer.data
    }
    return Response(data)
    
# Create your views here.
@api_view(['GET'])
def Basicsearch(request):
    query  = request.GET.get('query')

    books = Book.objects.filter(Q(book_name__icontains=query) | Q(description__icontains=query))
    serializer = BookSerializer(books, many=True)
    
    data = {
        "Keyword": query,
        "results": serializer.data
    }
    return Response(data)

