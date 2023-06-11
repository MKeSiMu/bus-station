from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from station.models import Bus
from station.serializers import BusSerializer


@api_view(["GET", "POST"])
def bus_list(request):
    if request.method == "GET":
        movies = Bus.objects.all()
        serializer = BusSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        serializer = BusSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def bus_detail(request, pk):
    queryset = Bus.objects.all()
    movie = get_object_or_404(queryset, pk=pk)

    if request.method == "GET":
        serializer = BusSerializer(movie)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = BusSerializer(movie, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    if request.method == "DELETE":
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
