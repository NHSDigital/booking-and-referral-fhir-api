from black import T
import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example
import re
import uuid
import base64
import json


class TestAppointment:
    existing_appointment_id = "c3f6145e-1a26-4345-b3f2-dccbcba62049"
    non_existing_appointment_id = str(uuid.uuid4())
    nhsd_token = "nhsd-token"

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_appointments(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("appointment/GET-success.json")
        patient_id = "4857773456"
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            params={"patientIdentifier": patient_id},
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
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
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("appointment/id/GET-success.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_appointment_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_appointment_entity_not_found(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 403
        expected_body = load_example("entity-not-found.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.non_existing_appointment_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_create_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 201
        expected_res_body = load_example("appointment/POST-success.txt")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            json=load_example("appointment/POST-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

        response = response.content.decode("utf-8").strip()
        actual_content = re.sub("\"", "", response)  # FastApi adds double quote to text response

        assert_that(expected_res_body).is_equal_to(actual_content)

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_put_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            json=load_example("appointment/id/PUT-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_patch_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.patch(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            json=load_example("appointment/id/PATCH-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_delete_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_put_appointment_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
            json=load_example("appointment/id/PUT-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_put_appointment_entity_not_found(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 403
        expected_body = load_example("entity-not-found.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.non_existing_appointment_id}",
            json=load_example("appointment/id/PUT-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_patch_appointment_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.patch(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
            json=load_example("appointment/id/PATCH-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_patch_appointment_entity_not_found(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 403
        expected_body = load_example("entity-not-found.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.patch(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.non_existing_appointment_id}",
            json=load_example("appointment/id/PATCH-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_delete_appointment_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_delete_appointment_entity_not_found(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 403
        expected_body = load_example("entity-not-found.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.non_existing_appointment_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_appointments_method_not_allowed(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")
        patient_id = "4857773456"
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            params={"patientIdentifier": patient_id},
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_appointment_id_method_not_allowed(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 405
        expected_body = load_example("method-not-allowed.json")
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "NHSD-Token": self.nhsd_token,
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
