import pytest
import requests
from .configuration import config
from assertpy import assert_that
from .example_loader import load_example
from datetime import datetime


class TestReceiverErrors:
    currentTime = datetime.now()
    nhsd_token = "nhsd-token"

    @pytest.mark.errors
    @pytest.mark.integration
    def test_401_unauthorized_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 401
        expected_body = load_example("unauthorized.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-401",
                "NHSD-Token": self.nhsd_token,
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

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-403",
                "NHSD-Token": self.nhsd_token,
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

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-406",
                "NHSD-Token": self.nhsd_token,
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

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-409",
                "NHSD-Token": self.nhsd_token,
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

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-422",
                "NHSD-Token": self.nhsd_token,
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
    def test_500_server_error_error(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 500
        expected_body = load_example("server-error.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-500",
                "NHSD-Token": self.nhsd_token,
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

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-501",
                "NHSD-Token": self.nhsd_token,
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
        expected_body = load_example("unavailable.json")

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/Slot",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001-503",
                "NHSD-Token": self.nhsd_token,
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
