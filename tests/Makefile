-include .env

JWT_PRIVATE_KEY_ABSOLUTE_PATH ?= $(shell pwd)/jwtRS512.key
APIGEE_API_TOKEN ?= $(shell export SSO_LOGIN_URL=https://login.apigee.com && eval get_token -u $(APIGEE_USERNAME))

OAUTH_BASE_URI=https://$(APIGEE_ENVIRONMENT).api.service.nhs.uk
OAUTH_PROXY=oauth2
REDIRECT_URL=https://nhsd-apim-testing-internal-dev.herokuapp.com/callback

.EXPORT_ALL_VARIABLES:

run:
	poetry run pytest -s -v $(f);

#  run tests with certain marker e.g. make run-sandbox runs tests marked with sandbox
run-%:
	poetry run pytest -s -v -m "$*" $(f)