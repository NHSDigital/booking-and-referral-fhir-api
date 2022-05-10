SERVICE_NAME = booking-and-referral-$(APIGEE_ENVIRONMENT)
PROXY_BASE_PATH = 'booking-and-referral/FHIR/R4'

PRIVATE_KEY_FILE ?= $(shell pwd)/jwtRS512.key

OAUTH_BASE_URI=https://$(APIGEE_ENVIRONMENT).api.service.nhs.uk


-include .env
TOKEN ?= $(shell eval get_token -u $(APIGEE_USERNAME))

export JWT_PRIVATE_KEY_ABSOLUTE_PATH= $(PRIVATE_KEY_FILE)

export APIGEE_API_TOKEN=$(TOKEN) 

CUSTOM_CMD_OPT = --service-name="$(SERVICE_NAME)" \
                 --default-client-id="$(DEFAULT_CLIENT_ID)" --default-client-secret="$(DEFAULT_CLIENT_SECRET)" \
                 --default-callback-url="$(DEFAULT_CALLBACK_URL)" --apigee-environment="$(APIGEE_ENVIRONMENT)" \
                 --apigee-api-token="$(TOKEN)" --pr-no=$(PR_NO) --proxy-base-path=$(PROXY_BASE_PATH) \
                 --jwt-private-key-file=$(PRIVATE_KEY_FILE) --oauth-base-uri=$(OAUTH_BASE_URI)\
				 --oauth-proxy=$(OAUTH_PROXY)

reruns = 0

run:
	../.venv/bin/pytest -s -v test_appointment.py::TestAppointment::test_get_appointments --reruns $(reruns) $(CUSTOM_CMD_OPT) $(f)

run-%:
	../.venv/bin/pytest -s -v --reruns $(reruns) $(CUSTOM_CMD_OPT) -m $(subst run-,,$@)

echo-cmd:
	echo ../.venv/bin/pytest -s -v --reruns $(reruns) $(CUSTOM_CMD_OPT) $(f)
