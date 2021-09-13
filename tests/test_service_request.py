import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example


class TestServiceRequest:
    existing_referral_id = "some-id"

    @pytest.mark.service_request
    @pytest.mark.integration
    def test_get_referrals(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("service_request/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    def test_get_referral(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("service_request/id/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{self.existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    def test_create_referral(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 201
        expected_body = ""

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.service_request
    @pytest.mark.integration
    def test_put_referral(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("service_request/id/PUT-success.json")

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{self.existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    def test_patch_referral(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("service_request/id/PATCH-success.json")

        # When
        response = requests.patch(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{self.existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    def test_delete_referral(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = ""

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{self.existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))
