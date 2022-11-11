import pytest


class TestProcessMessage:
    target_id = "NHS0001"

    @pytest.mark.target_identifier
    @pytest.mark.integration
    @pytest.mark.sandbox
    def test_create_process_message(self, get_token_client_credentials):
        pass
