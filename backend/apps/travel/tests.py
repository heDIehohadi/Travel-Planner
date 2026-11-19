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
            type=Destination.DestinationType.CITY,
        )

        self.destination = Destination.objects.create(
            name="Shiraz",
            type=Destination.DestinationType.CITY,
        )

        self.other_origin = Destination.objects.create(
            name="Rasht",
            type=Destination.DestinationType.CITY,
        )

        self.client.force_authenticate(
            user=self.user
        )

    # -------------------------
    # LIST
    # -------------------------

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
            budget_min=100000,
            budget_max=200000,
            currency="IRR",
        )

        TravelPlan.objects.create(
            user=self.other_user,
            origin=self.other_origin,
            destination=self.destination,
            budget_min=200000,
            budget_max=300000,
            currency="IRR",
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
            response.data[0]["budget_min"],
            "100000.00",
        )

    # -------------------------
    # CREATE
    # -------------------------

    def test_authenticated_user_can_create_travel_plan(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "origin": self.origin.id,
                "destination": self.destination.id,
                "travel_date_from": "2026-10-01",
                "travel_date_to": "2026-10-07",
                "budget_min": "100000.00",
                "budget_max": "200000.00",
                "currency": "IRR",
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
                "budget_min": "100000.00",
                "budget_max": "200000.00",
                "currency": "IRR",
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

    # -------------------------
    # RETRIEVE
    # -------------------------

    def test_user_can_retrieve_their_own_travel_plan(self):
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget_min=100000,
            budget_max=200000,
            currency="IRR",
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
            budget_min=200000,
            budget_max=300000,
            currency="IRR",
        )

        response = self.client.get(
            f"/travel/plans/{other_plan.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    # -------------------------
    # UPDATE
    # -------------------------

    def test_user_can_update_their_own_travel_plan_with_put(self):
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget_min=100000,
            budget_max=200000,
            currency="IRR",
        )

        response = self.client.put(
            f"/travel/plans/{travel_plan.id}/",
            {
                "origin": self.other_origin.id,
                "destination": self.destination.id,
                "travel_date_from": "2026-11-01",
                "travel_date_to": "2026-11-10",
                "budget_min": "300000.00",
                "budget_max": "500000.00",
                "currency": "IRR",
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
            travel_plan.budget_min,
            300000,
        )

        self.assertEqual(
            travel_plan.budget_max,
            500000,
        )

    def test_user_can_partially_update_their_own_travel_plan(self):
        travel_plan = TravelPlan.objects.create(
            user=self.user,
            origin=self.origin,
            destination=self.destination,
            budget_min=100000,
            budget_max=200000,
            currency="IRR",
        )

        response = self.client.patch(
            f"/travel/plans/{travel_plan.id}/",
            {
                "budget_min": "500000.00",
                "budget_max": "700000.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        travel_plan.refresh_from_db()

        self.assertEqual(
            travel_plan.budget_min,
            500000,
        )

        self.assertEqual(
            travel_plan.budget_max,
            700000,
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
            budget_min=200000,
            budget_max=300000,
            currency="IRR",
        )

        response = self.client.patch(
            f"/travel/plans/{other_plan.id}/",
            {
                "budget_min": "900000.00",
                "budget_max": "999999.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        other_plan.refresh_from_db()

        self.assertEqual(
            other_plan.budget_min,
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
            budget_min=100000,
            budget_max=200000,
            currency="IRR",
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

    def test_user_cannot_delete_another_users_travel_plan(self):
        other_plan = TravelPlan.objects.create(
            user=self.other_user,
            origin=self.origin,
            destination=self.destination,
            budget_min=200000,
            budget_max=300000,
            currency="IRR",
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
                "budget_min": "100000.00",
                "budget_max": "200000.00",
                "currency": "IRR",
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

    def test_origin_is_optional(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "destination": self.destination.id,
                "budget_min": "100000.00",
                "budget_max": "200000.00",
                "currency": "IRR",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_destination_is_optional_when_budget_is_provided(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "budget_min": "100000.00",
                "budget_max": "200000.00",
                "currency": "IRR",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_destination_is_optional_when_dates_are_provided(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "travel_date_from": "2026-12-10",
                "travel_date_to": "2026-12-15",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_at_least_one_of_destination_budget_or_dates_is_required(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "origin": self.origin.id,
                "currency": "IRR",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_travel_date_from_cannot_be_after_travel_date_to(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "destination": self.destination.id,
                "travel_date_from": "2026-10-20",
                "travel_date_to": "2026-10-10",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_budget_min_cannot_be_greater_than_budget_max(self):
        response = self.client.post(
            "/travel/plans/",
            {
                "destination": self.destination.id,
                "budget_min": "500000.00",
                "budget_max": "300000.00",
                "currency": "IRR",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
    def test_patch_unrelated_field_keeps_saved_destination(self):
        plan = TravelPlan.objects.create(
            user=self.user,
            destination=self.destination,
        )

        response = self.client.patch(
            f"/travel/plans/{plan.id}/",
            {"currency": "IRR"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_patch_cannot_remove_the_only_input(self):
        plan = TravelPlan.objects.create(
            user=self.user,
            destination=self.destination,
        )

        response = self.client.patch(
            f"/travel/plans/{plan.id}/",
            {"destination": None},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )    