import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example


class TestAppointment:
    existing_appointment_id = "c3f6145e-1a26-4345-b3f2-dccbcba62049"

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_get_appointments(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("appointment/GET-success.json")
        patient_id = "4857773456"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            params={"patientIdentifier": patient_id},
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_get_appointments_missing_param_patient_id(
        self, get_token_client_credentials
    ):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_get_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("appointment/id/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_get_appointment_bad_id(self, get_token_client_credentials):
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
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    @pytest.mark.debug
    def test_create_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 201
        expected_res_body = load_example("appointment/POST-success.txt")

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment",
            json=load_example("appointment/POST-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

        actual_content = response.content.decode("utf-8").strip()
        print(f"act {actual_content}")
        print(f"exp {expected_res_body}")

        assert_that(expected_res_body).is_equal_to(actual_content)

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_put_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            json=load_example("appointment/id/PUT-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_patch_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'

        # When
        response = requests.patch(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            json=load_example("appointment/id/PATCH-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_delete_appointment(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{self.existing_appointment_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_put_appointment_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
            json=load_example("appointment/id/PUT-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_patch_appointment_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.patch(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
            json=load_example("appointment/id/PATCH-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.appointment
    @pytest.mark.integration
    def test_delete_appointment_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Appointment/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
