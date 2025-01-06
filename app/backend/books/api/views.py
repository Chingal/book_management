from bson import ObjectId, errors

from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.accounts.auth import CustomTokenAuthentication
from .serializers import BookSerializer, AveragePriceSerializer
from .pagination import CustomPageNumberPagination
from ..managers import BookManager
from ..models import Book


class BookListView(ListCreateAPIView):
    """
    View to list all books with optional filtering and pagination
    """
    #authentication_classes = [CustomTokenAuthentication]
    name = 'Book List'
    pagination_class = CustomPageNumberPagination
    #permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Returns a queryset of books filtered by optional query parameters.
        """
        manager = BookManager()
        filter_query = {}

        if "title" in self.request.GET:
            filter_query["title"] = self.request.GET["title"]
        if "author" in self.request.GET:
            filter_query["author"] = self.request.GET["author"]

        return manager.all(filter_query)


class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve details, update and destroy of a specific book
    """
    #authentication_classes = [CustomTokenAuthentication]
    name = 'Manage Book APIView'
    manager = BookManager()
    pagination_class = CustomPageNumberPagination
    #permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        """
        Retrieves the list of books from MongoDB using the BookManager.
        """
        return self.manager.all({})

    def get_object(self):
        """
        Retrieves a single book based on its ID from MongoDB.
        """
        book_id = self.kwargs.get("id")
        try:
            book_id = ObjectId(book_id)
        except errors.InvalidId:
            raise NotFound(f"Book with ID {book_id} is not a valid ObjectId.")

        book = self.manager.get(id=book_id)
        if not book:
            raise NotFound(f"Book with ID {book_id} not found")

        return book

    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific book based on its ID from MongoDB.
        """
        book_id = self.kwargs.get("id")

        deleted = self.manager.delete(book_id)
        if not deleted:
            raise NotFound(f"Book with ID {book_id} not found.")

        return Response(status=status.HTTP_204_NO_CONTENT)


class AveragePriceAPIView(APIView):
    """
    API View to calculate the average price of books for a given year.
    """
    #authentication_classes = [CustomTokenAuthentication]
    name = 'Average price'
    manager = BookManager()
    #permission_classes = [IsAuthenticated]

    def get(self, request, year, version=None):
        """
        Handles GET requests to calculate the average price of books published in a specific year.

        :param request: HTTP request object
        :param year: (int) The year for which the average price of books is to be calculated.
        :param version: (str, optional) The API version (if applicable).

        :return: Response A Response object containing the average price for the specified year or an error message.
        """
        try:
            year = int(year)
            if year < 1000 or year > 9999:
                raise ValueError("Year must be a 4-digit number.")
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid year format. Year must be a 4-digit number."},
                status=status.HTTP_400_BAD_REQUEST
            )

        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)

        pipeline = [
            {
                "$match": {
                    "published_date": {
                        "$gte": start_date,
                        "$lt": end_date,
                    }
                }
            },
            {
                "$group": {
                    "_id": None,
                    "average_price": {"$avg": "$price"},
                }
            }
        ]

        try:
            collection = self.manager.raw_collection
            result = list(collection.aggregate(pipeline))
        except Exception as e:
            return Response(
                {"error": f"Database query failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        average_price = result[0].get("average_price", 0.0) if result else 0.0
        response_data = {"year": year, "average_price": average_price}

        serializer = AveragePriceSerializer(data=response_data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
