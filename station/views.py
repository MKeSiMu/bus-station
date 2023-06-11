from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from station.models import Bus
from station.serializers import BusSerializer

"""
func base view
"""

# @api_view(["GET", "POST"])
# def bus_list(request):
#     if request.method == "GET":
#         buses = Bus.objects.all()
#         serializer = BusSerializer(buses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == "POST":
#         serializer = BusSerializer(data=request.data)
#
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# def bus_detail(request, pk):
#     queryset = Bus.objects.all()
#     bus = get_object_or_404(queryset, pk=pk)
#
#     if request.method == "GET":
#         serializer = BusSerializer(bus)
#         return Response(serializer.data)
#
#     if request.method == "PUT":
#         serializer = BusSerializer(bus, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     if request.method == "DELETE":
#         bus.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


"""
class base APIView
"""

# class BusList(APIView):
#     def get(self, request):
#         buses = Bus.objects.all()
#         serializer = BusSerializer(buses, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = BusSerializer(data=request.data)
#
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# class BusDetail(APIView):
#     def get_object(self, pk):
#         queryset = Bus.objects.all()
#         bus = get_object_or_404(queryset, pk=pk)
#         return bus
#
#     def get(self, request, pk):
#         bus = self.get_object(pk)
#         serializer = BusSerializer(bus)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         bus = self.get_object(pk)
#         serializer = BusSerializer(bus, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, pk):
#         bus = self.get_object(pk)
#         bus.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



"""
class base GenericAPIView + Mixins
"""


# class BusList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class BusDetail(
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


"""
class base Generic Views
"""


class BusList(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer


class BusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
