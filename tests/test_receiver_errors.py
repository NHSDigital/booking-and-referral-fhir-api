import base64
import json
from datetime import datetime

import pytest
import requests
from assertpy import assert_that

from .configuration import config
from .example_loader import load_example


class TestReceiverErrors:
    currentTime = datetime.now()

    @pytest.mark.errors
    @pytest.mark.integration
    def test_401_unauthorized_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 401
        expected_body = load_example("unauthorized.json")
        target_identifier = json.dumps({"value": "NHS0001-401", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_403_forbidden_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 403
        expected_body = load_example("forbidden.json")
        target_identifier = json.dumps({"value": "NHS0001-403", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_406_not_acceptable_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 406
        expected_body = load_example("not-acceptable.json")
        target_identifier = json.dumps({"value": "NHS0001-406", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_408_timeout_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 408
        expected_body = load_example("OperationOutcome/REC/408-REC_TIMEOUT-timeout.json")
        target_identifier = json.dumps({"value": "NHS0001-408", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_409_conflict_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 409
        expected_body = load_example("conflict.json")
        target_identifier = json.dumps({"value": "NHS0001-409", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_422_unprocessable_entity_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 422
        expected_body = load_example("unprocessable-entity.json")
        target_identifier = json.dumps({"value": "NHS0001-422", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_500_server_error_exception_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 500
        expected_body = load_example("OperationOutcome/REC/500-REC_SERVER_ERROR-exception.json")
        target_identifier = json.dumps({"value": "NHS0001-500", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_500_server_error_no_store_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 500
        expected_body = load_example("OperationOutcome/REC/500-REC_SERVER_ERROR-no-store.json")
        target_identifier = json.dumps({"value": "NHS0001-500-2", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_501_not_implemented_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 501
        expected_body = load_example("not-implemented.json")
        target_identifier = json.dumps({"value": "NHS0001-501", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())

    @pytest.mark.errors
    @pytest.mark.integration
    def test_503_unavailable_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 503
        expected_body = load_example("OperationOutcome/REC/503-REC_SERVICE_UNAVAILABLE-exception.json")
        target_identifier = json.dumps({"value": "NHS0001-503", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689"
            },
            params={
                "healthcareService": "09a01679-2564-0fb4-5129-aecc81ea2706",
                "status": ["free"],
                "start": self.currentTime,
                "end": self.currentTime,
                "_include": ["Schedule"],
            },
        )

        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)
        assert_that(expected_body).is_equal_to(response.json())
