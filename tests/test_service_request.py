import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example


class TestServiceRequest:
    existing_referral_id = "5dfbbdb8-f94b-4113-b3ff-249cac7f0694"
    existing_patient_id = "4857773456"

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_referrals(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("service_request/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest",
            params={"patientIdentifier": self.existing_patient_id},
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
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
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_referral_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_create_referral(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 201
        expected_body = '""'

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest",
            json=load_example("service_request/POST-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
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
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
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
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_delete_referral(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{self.existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_put_referral_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_patch_referral_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.patch(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_delete_referral_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
