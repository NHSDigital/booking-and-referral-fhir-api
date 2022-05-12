-include .env

# to run against a PR:
#FULLY_QUALIFIED_SERVICE_NAME=booking-and-referral-pr-92
#SERVICE_BASE_PATH =booking-and-referral/FHIR/R4-pr-92

FULLY_QUALIFIED_SERVICE_NAME = booking-and-referral-$(APIGEE_ENVIRONMENT)
SERVICE_BASE_PATH = 'booking-and-referral/FHIR/R4'

JWT_PRIVATE_KEY_ABSOLUTE_PATH ?= $(shell pwd)/jwtRS512.key
APIGEE_API_TOKEN ?= $(shell export SSO_LOGIN_URL=https://login.apigee.com && eval get_token -u $(APIGEE_USERNAME))

# set env vars
export OAUTH_BASE_URI=https://$(APIGEE_ENVIRONMENT).api.service.nhs.uk
export APIGEE_API_TOKEN
export JWT_PRIVATE_KEY_ABSOLUTE_PATH
export OAUTH_PROXY

CUSTOM_CMD_OPT = --service-name="$(FULLY_QUALIFIED_SERVICE_NAME)" \
                 --default-client-id="$(CLIENT_ID)" --default-client-secret="$(CLIENT_SECRET)" \
                 --default-callback-url="$(REDIRECT_URL)" --apigee-environment="$(APIGEE_ENVIRONMENT)" \
				 --proxy-base-path=$(SERVICE_BASE_PATH) --oauth-base-uri=$(OAUTH_BASE_URI)\

reruns = 0

run:
	../.venv/bin/pytest -s -v --reruns $(reruns) $(CUSTOM_CMD_OPT) $(f)

run-%:
	../.venv/bin/pytest -s -v --reruns $(reruns) $(CUSTOM_CMD_OPT) -m $(subst run-,,$@)

echo-cmd:
	echo ../.venv/bin/pytest -s -v --reruns $(reruns) $(CUSTOM_CMD_OPT) $(f)
