import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example


class TestDocumentReference:
    existing_document_reference_id = "c3f6145e-1a26-4345-b3f2-dccbcba62049"

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_document_reference(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("document_reference/GET-success.json")
        patient_id = "4857773456"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference",
            params={"patientIdentifier": patient_id},
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_document_reference_missing_param_patient_id(
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

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_document_reference_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = load_example("document_reference/id/GET-success.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{self.existing_document_reference_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_get_document_reference_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_post_document_reference(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 201

        # When
        response = requests.post(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference",
            json=load_example("document_reference/POST-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_put_document_reference(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{self.existing_document_reference_id}",
            json=load_example("document_reference/id/PUT-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_delete_document_reference(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 200
        expected_body = '""'

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{self.existing_document_reference_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.content.decode("utf-8"))

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_put_document_reference_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.put(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{bad_id}",
            json=load_example("document_reference/id/PUT-body.json"),
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.document_reference
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_delete_document_reference_bad_id(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400
        expected_body = load_example("bad-request.json")
        bad_id = "non-uuid"

        # When
        response = requests.delete(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/DocumentReference/{bad_id}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-ServiceIdentifier": "NHS0001",
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
