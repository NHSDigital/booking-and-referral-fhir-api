import requests
from assertpy import assert_that
import asyncio
import pytest
import base64
import json


class TestEndpoints:
    @pytest.mark.auth
    def test_invalid_access_token(self, base_url_path):
        expected_status_code = 403
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{base_url_path}/metadata",
            headers={
                "Authorization": "Bearer invalid_token",
                "NHSD-Target-Identifier": target_identifier_encoded,
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.auth
    def test_missing_access_token(self, base_url_path):
        expected_status_code = 401
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{base_url_path}/metadata",
            headers={
                "Authorization": "",
                "NHSD-Target-Identifier": target_identifier_encoded,
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
    def test_invalid_nhsd_service_identifier(self, get_token_client_credentials, base_url_path):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 500
        target_identifier = json.dumps({"value": "invalid", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{base_url_path}/metadata",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
        )
        # Then
        assert_that(expected_status_code).is_equal_to(response.status_code)

    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_endpoint_not_found(self, get_token_client_credentials, base_url_path):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_status_code = 404
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        # When
        response = requests.get(
            url=f"{base_url_path}/invalid",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
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
        self, get_token_client_credentials, debug, path_suffix, base_url_path, cmd_options
    ):
        # Given
        token = get_token_client_credentials["access_token"]
        expected_target = f"https://{cmd_options['--apigee-environment']}.api.service.nhs.uk/bars-mock-receiver-proxy/{path_suffix}"
        target_identifier = json.dumps({"value": "NHS0001", "system": "tests"})
        target_identifier_encoded = base64.b64encode(bytes(target_identifier, "utf-8"))

        await debug.start_trace()

        # When
        requests.get(
            url=f"{base_url_path}/{path_suffix}",
            headers={
                "Authorization": f"Bearer {token}",
                "NHSD-Target-Identifier": target_identifier_encoded,
                "X-Request-Id": "c1ab3fba-6bae-4ba4-b257-5a87c44d4a91",
                "X-Correlation-Id": "9562466f-c982-4bd5-bb0e-255e9f5e6689",
            },
        )

        target = await debug.get_apigee_variable_from_trace(name="target.url")

        # Then
        assert_that(target).is_equal_to(expected_target)
