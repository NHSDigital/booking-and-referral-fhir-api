import base64
import json
import uuid

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestServiceRequest:
    existing_referral_id = "c3f6145e-1a26-4345-b3f2-dccbcba62049"
    non_existing_referral_id = str(uuid.uuid4())
    existing_patient_id = "4857773456"

    target_id = json.dumps({"value": "NHS0001", "system": config.TARGET_SYSTEM})
    target_id_encoded = base64.b64encode(bytes(target_id, "utf-8"))

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_referrals(self, get_token_client_credentials):
        """
           test to get a list of services for the nhs_number associated /serviceRequest?patient:identifier=12312
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("service_request/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest",
            params={"patient:identifier": self.existing_patient_id},
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_referral(self, get_token_client_credentials):
        """
           test to get a service related to the nhs_number serviceRequest?patient:identifier=12312
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("service_request/id/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{self.existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_referral_bad_id(self, get_token_client_credentials):
        """
           test to check the response when the request contains an invalid nhs_number
        """
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
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_referral_entity_not_found(self, get_token_client_credentials):
        """
           test to check the response when the request contains an invalid referral number
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404
        expected_body = load_example("OperationOutcome/REC/404-REC_NOT_FOUND-not-found.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.non_existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_referrals_method_not_allowed(self, get_token_client_credentials):
        """
           test to check the put method is not allowed for serviceRequest
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest",
            params={"patient:identifier": self.existing_patient_id},
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.service_request
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_referral_id_method_not_allowed(self, get_token_client_credentials):
        """
           test to check the post method is not allowed for serviceRequest
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/ServiceRequest/{self.existing_referral_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": self.target_id_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
