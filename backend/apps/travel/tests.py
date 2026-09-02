from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import Destination, TravelPlan

class TravelPlanAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        User = get_user_model()

        self.user = User.objects.create_user(
            phone_number="09120000000",
        )
        self.other_user = User.objects.create_user(
            phone_number="09121111111",
        )
        self.origin = Destination.objects.create(
            name="Tehran",
        )
        self.destination = Destination.objects.create(
            name="Shiraz",
        )
        self.other_origin = Destination.objects.create(
            name="Rasht",
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_authenticated_user_can_list_travel_plans(self):
        response = self.client.get(
            "/travel/plans/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_user_can_only_see_their_own_travel_plans(self):
        TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget=100000,
        )

        TravelPlan.objects.create(
            user=self.other_user,
            origin=self.other_origin,
            destination=self.destination,
            budget=200000,
        )

        response = self.client.get(
            "/travel/plans/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["budget"],
            100000,
        )

    def test_authenticated_user_can_create_travel_plan(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "origin": self.origin.id,
                "destination": self.destination.id,
                "budget": 100000,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_created_travel_plan_belongs_to_authenticated_user(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "origin": self.origin.id,
                "destination": self.destination.id,
                "budget": 100000,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        travel_plan = TravelPlan.objects.get(
            id=response.data["id"]
        )

        self.assertEqual(
            travel_plan.user,
            self.user,
        )

    def test_user_can_retrieve_their_own_travel_plan(self):
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget=100000,
        )

        response = self.client.get(
            f"/travel/plans/{travel_plan.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            travel_plan.id,
        )

    def test_user_cannot_retrieve_another_users_travel_plan(self):
        other_plan = TravelPlan.objects.create(
            user=self.other_user,
            origin=self.origin,
            destination=self.destination,
            budget=200000,
        )

        response = self.client.get(
            f"/travel/plans/{other_plan.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_user_can_update_their_own_travel_plan_with_put(self):
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget=100000,
        )

        response = self.client.put(
            f"/travel/plans/{travel_plan.id}/",
            {
                "origin": self.other_origin.id,
                "destination": self.destination.id,
                "budget": 300000,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        travel_plan.refresh_from_db()

        self.assertEqual(
            travel_plan.origin,
            self.other_origin,
        )

        self.assertEqual(
            travel_plan.destination,
            self.destination,
        )

        self.assertEqual(
            travel_plan.budget,
            300000,
        )

    def test_user_can_partially_update_their_own_travel_plan(self):
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget=100000,
        )

        response = self.client.patch(
            f"/travel/plans/{travel_plan.id}/",
            {
                "budget": 500000,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        travel_plan.refresh_from_db()

        self.assertEqual(
            travel_plan.budget,
            500000,
        )

        self.assertEqual(
            travel_plan.origin,
            self.origin,
        )

        self.assertEqual(
            travel_plan.destination,
            self.destination,
        )

    def test_user_cannot_update_another_users_travel_plan(self):
        other_plan = TravelPlan.objects.create(
            user=self.other_user,
            origin=self.origin,
            destination=self.destination,
            budget=200000,
        )

        response = self.client.patch(
            f"/travel/plans/{other_plan.id}/",
            {
                "budget": 999999,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        other_plan.refresh_from_db()

        self.assertEqual(
            other_plan.budget,
            200000,
        )

    # -------------------------
    # DELETE
    # -------------------------

    def test_user_can_delete_their_own_travel_plan(self):
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget=100000,
        )

        response = self.client.delete(
            f"/travel/plans/{travel_plan.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            TravelPlan.objects.filter(
                id=travel_plan.id
            ).exists()
        )

    # -------------------------
    # USER ISOLATION - DELETE
    # -------------------------

    def test_user_cannot_delete_another_users_travel_plan(self):
        other_plan = TravelPlan.objects.create(
            user=self.other_user,
            origin=self.origin,
            destination=self.destination,
            budget=200000,
        )

        response = self.client.delete(
            f"/travel/plans/{other_plan.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            TravelPlan.objects.filter(
                id=other_plan.id
            ).exists()
        )

    # -------------------------
    # AUTHENTICATION
    # -------------------------

    def test_unauthenticated_user_cannot_list_travel_plans(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            "/travel/plans/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_create_travel_plan(self):
        self.client.force_authenticate(user=None)

        response = self.client.post(
            "/travel/plans/",
            {
                "origin": self.origin.id,
                "destination": self.destination.id,
                "budget": 100000,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    # -------------------------
    # VALIDATION
    # -------------------------

    def test_origin_is_required(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "destination": self.destination.id,
                "budget": 100000,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_destination_is_required(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "origin": self.origin.id,
                "budget": 100000,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )