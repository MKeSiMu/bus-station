from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APIClient

from station.models import Bus, Facility
from station.serializers import BusSerializer, BusListSerializer, BusDetailSerializer

BUS_URL = reverse("station:bus-list")


def detail_url(bus_id: int):
    return reverse("station:bus-detail", args=[bus_id])


def sample_bus(**params):
    defaults = {
        "info": "Sample Bus",
        "num_seats": 20,
    }

    defaults.update(params)

    return Bus.objects.create(**defaults)


class UnauthenticatedBusApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(BUS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedBusApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@teset.com",
            "testpass"
        )
        self.client.force_authenticate(self.user)

    def test_list_buses(self):
        sample_bus()
        bus_with_facilities = sample_bus()

        facility1 = Facility.objects.create(name="Wi-Fi")
        facility2 = Facility.objects.create(name="WC")

        bus_with_facilities.facilities.add(facility1, facility2)

        res = self.client.get(BUS_URL)

        buses = Bus.objects.all()
        serializer = BusListSerializer(buses, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_buses_by_facilities(self):
        bus1 = sample_bus(info="Bus 1")
        bus2 = sample_bus(info="Bus 2")

        facility1 = Facility.objects.create(name="Wi-Fi")
        facility2 = Facility.objects.create(name="WC")

        bus1.facilities.add(facility1)
        bus2.facilities.add(facility2)

        bus3 = sample_bus(info="Bus without facilities")

        res = self.client.get(BUS_URL, {"facilities": f"{facility1.id},{facility2.id}"})

        serializer1 = BusListSerializer(bus1)
        serializer2 = BusListSerializer(bus2)
        serializer3 = BusListSerializer(bus3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_retrieve_bus_detail(self):
        bus = sample_bus()
        bus.facilities.add(Facility.objects.create(name="Wi-Fi"))

        url = detail_url(bus.id)

        res = self.client.get(url)

        serializer = BusDetailSerializer(bus)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_bus_forbidden(self):
        payload = {
            "info": "Bus",
            "num_seats": 15
        }

        res = self.client.post(BUS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBusApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_bus(self):
        payload = {
            "info": "Bus",
            "num_seats": 15
        }

        res = self.client.post(BUS_URL, payload)
        bus = Bus.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(bus, key))

    def test_create_bus(self):
        facility1 = Facility.objects.create(name="Wi-Fi")
        facility2 = Facility.objects.create(name="WC")

        payload = {
            "info": "Bus",
            "num_seats": 15,
            "facilities": [facility1.id, facility2.id]
        }

        res = self.client.post(BUS_URL, payload)
        bus = Bus.objects.get(id=res.data["id"])
        facilities = bus.facilities.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(facilities.count(), 2)
        self.assertIn(facility1, facilities)
        self.assertIn(facility2, facilities)

    def test_delete_bus_not_allowed(self):  #TODO: need to change in views viewsets.ModelViewSet to class base GenericViewSets without Destroy
        bus = sample_bus()

        url = detail_url(bus.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
