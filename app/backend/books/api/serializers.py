from datetime import datetime, date
from rest_framework import serializers
from rest_framework.fields import DateField

from ..models import Book
from ..managers import BookManager

class FlexibleDateField(DateField):
    """
    Serializer to representate flexible DateField
    """
    def to_representation(self, value):
        if isinstance(value, datetime):
            return value.date()
        return super().to_representation(value)


class BookSerializer(serializers.Serializer):
    """
    Serializer for the Book model.
    Transforms and validates book data for API responses.
    """
    id = serializers.CharField(read_only=True)
    title = serializers.CharField()
    author = serializers.CharField()
    published_date = FlexibleDateField()
    genre = serializers.CharField(allow_null=True)
    price = serializers.FloatField()

    def create(self, validated_data):
        """
        Save a new book document in MongoDB
        """
        book_instance = Book(**validated_data)
        book_instance.save()
        return validated_data

    def update(self, instance, validated_data):
        """
        Update an existing book document in MongoDB.
        """
        manager = BookManager()

        published_date = validated_data.get("published_date")
        if isinstance(published_date, date):
            published_date = datetime.combine(published_date, datetime.min.time())

        book_data = {
            "title": validated_data.get("title"),
            "author": validated_data.get("author"),
            "published_date": published_date,
            "genre": validated_data.get("genre"),
            "price": validated_data.get("price"),
        }
        manager.update(instance.id, book_data)

        return book_data


class AveragePriceSerializer(serializers.Serializer):
    """
    Serializer to calculate average book prices
    """
    year = serializers.IntegerField(min_value=1000, max_value=9999)
    average_price = serializers.FloatField(min_value=0.0)
