import requests
from assertpy import assert_that
from .configuration import config
import asyncio
import pytest


class TestEndpoints:

    @pytest.mark.auth
    def test_invalid_access_token(self):
        expected_status_code = 401

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": "Bearer invalid_token",
                "NHSD-Service": "NHS0001",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.auth
    def test_invalid_access_token_auth_code(self, default_oauth_helper):
        # This test checks that when trying to authenticate using auth_code flow
        # an exemption is rised. Sadly the method get_token_response doesn't return
        # the 401 error from apigee and raises and error instead.
        with pytest.raises(Exception):
            assert asyncio.run(
                default_oauth_helper.get_token_response(grant_type="authorization_code")
            )

    @pytest.mark.broker
    def test_invalid_nhsd_service_identifier(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 400

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/metadata",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "invalid",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_endpoint_not_found(self, get_token_client_credentials):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404

        # When
        response = requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/invalid",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.asyncio
    @pytest.mark.broker
    @pytest.mark.parametrize(
        "path_suffix",
        ("Appointment", "Appointment/some-id", "Appointment/some-id?param=value"),
    )
    async def test_proxy_routing(
            self, get_token_client_credentials, debug, path_suffix
    ):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_target = f"https://{config.ENVIRONMENT}.api.service.nhs.uk/bars-mock-receiver-proxy/{path_suffix}"

        await debug.start_trace()

        # When
        requests.get(
            url=f"{config.BASE_URL}/{config.BASE_PATH}/{path_suffix}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Service": "NHS0001",
            },
        )

        target = await debug.get_apigee_variable_from_trace(name="target.url")

        # Then
        assert_that(target).is_equal_to(expected_target)
