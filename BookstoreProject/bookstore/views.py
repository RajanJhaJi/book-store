from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer, AddBookSerializer
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage 
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
def get_books(request):
    data = Book.objects.all()

    # if query param contains "search" implement the search option
    search_param = request.query_params.get("search")
    if search_param:
        data = data.filter(Q(title__icontains=search_param) | Q(author__icontains=search_param))

    # no of books per page
    books_per_page = 10
    page = request.query_params.get('page',1)

    paginator = Paginator(data,books_per_page)

    try:
        # get the books of requested page
        books = paginator.page(page)
    except PageNotAnInteger:
        # if the page parameter not an integer, we'll show the first page
        books = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, we'll show the last page
        books = paginator.page(paginator.num_pages)
    
    serializer = BookSerializer(books,many=True)
    return Response({"books": serializer.data, "page": int(page), "pages": paginator.num_pages},status=status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_book(request):
    serializer = AddBookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# Its just an additional helper view to create multiple books at a time
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def list_books(request):
    try:
        books = request.data
        created_count = 0
        for book in books:
            serializer = AddBookSerializer(data=book)
            if serializer.is_valid():
                serializer.save()
                created_count += 1
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":f"Total {created_count} books got created count."},status=status.HTTP_201_CREATED)

    except Exception as e: 
        return Response({"error":e},status=status.HTTP_400_BAD_REQUEST)




