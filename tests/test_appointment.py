import base64
import json
import uuid

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestAppointment:
    existing_appointment_id = "c3f6145e-1a26-4345-b3f2-dccbcba62049"
    non_existing_appointment_id = str(uuid.uuid4())

    target_id = json.dumps({"value": "NHS0001", "system": config.TARGET_SYSTEM})
    target_id_encoded = base64.b64encode(bytes(target_id, "utf-8"))

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_appointments(self, get_token_client_credentials):
        """
           test for /appointment..  to get all appointments for the patient passed as parameter on the request - /Appointment?patient:identifier=12312
           must return a list of appointments for the patient
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("appointment/GET-success.json")
        patient_id = "4857773456"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            params={"patient:identifier": patient_id},
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
    def test_get_appointments_missing_param_patient_id(
        self, get_token_client_credentials
    ):
        """
           test to get an appointment for the patient with a patient parameter missing on the request
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
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
    def test_get_appointment(self, get_token_client_credentials):
        """
           test to get an appointment for the patient passed as a parameter on the request
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("appointment/id/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
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
    def test_get_appointment_bad_id(self, get_token_client_credentials):
        """
         test to get an appointment for the patient with an invalid patient_id parameter on the
         request - /Appointment?patient:identifier=INVALID_ID
      """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
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
    def test_get_appointment_entity_not_found(self, get_token_client_credentials):
        """
           test to get all appointments for the patient passed as a parameter on the request -
           must return a message of entity not found.
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404
        expected_body = load_example("OperationOutcome/REC/404-REC_NOT_FOUND-not-found.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.non_existing_appointment_id}",
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
    def test_appointments_method_not_allowed(self, get_token_client_credentials):
        """
           test put method it's not allowed on appointment endpoint
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")
        patient_id = "4857773456"

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            params={"patient:identifier": patient_id},
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
    def test_appointment_id_method_not_allowed(self, get_token_client_credentials):
        """
          test to post an appointment -
          must return a message of method not allowed
        """
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
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
