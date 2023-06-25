from django.db.models import Count, F
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, generics, mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from station.models import Bus, Trip, Facility, Ticket, Order
from station.permissions import IsAdminOrIsAuthenticatedReadOnly
from station.serializers import (
    BusSerializer,
    TripSerializer,
    TripListSerializer,
    FacilitySerializer,
    BusDetailSerializer,
    BusListSerializer,
    TripDetailSerializer, TicketSerializer, OrderSerializer, OrderListSerializer, BusImageSerializer,
)

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
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     if request.method == "PUT":
#         serializer = BusSerializer(bus, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
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


# class BusList(generics.ListCreateAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer


# class BusDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer


"""
class base GenericViewSets
"""


# class BusViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     viewsets.GenericViewSet
# ):
#     queryset = Bus.objects.all()
#     serializer_class = BusSerializer


"""
class base ViewSets
"""

# Anon None
# IsAuthenticated: list, retrieve
# IsAdmin: create, update, partial_update, destroy


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    # authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly, )
    # permission_classes = (IsAuthenticated, )

    # def get_permissions(self):
    #     if self.action in ("create", "update", "partial_update", "destroy"):
    #         return [IsAdminUser()]
    #
    #     return super().get_permissions()


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly, )

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of strings to list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset

        facilities = self.request.query_params.get("facilities")

        if facilities:
            facilities_ids = self._params_to_ints(facilities)
            queryset = queryset.filter(facilities__id__in=facilities_ids)

        if self.action in ("list", "retrieve"):
            queryset = queryset.prefetch_related("facilities")

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return BusListSerializer

        if self.action == "retrieve":
            return BusDetailSerializer

        if self.action == "upload_image":
            return BusImageSerializer

        return BusSerializer

    @action(methods=["POST"], detail=True, url_path="upload-image", permission_classes=[IsAdminUser])
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific bus"""
        bus = self.get_object()
        serializer = self.get_serializer(bus, data=self.request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    @extend_schema(
        parameters=[
            OpenApiParameter(
                "facilities",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by Facility id(ex. ?facilities=1,3)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly, )

    # N + 1 problem solved
    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = (
                queryset
                .select_related("bus")
                .annotate(tickets_available=F("bus__num_seats") - Count("tickets"))
            )
            return queryset

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return TripListSerializer

        if self.action == "retrieve":
            return TripDetailSerializer

        return TripSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly, )

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("list", "retrieve"):
            queryset = queryset.select_related("trip", "order")
            return queryset

        return queryset


class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly, )

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related("tickets__trip__bus")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
