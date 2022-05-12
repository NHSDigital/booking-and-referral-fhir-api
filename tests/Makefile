-include .env

JWT_PRIVATE_KEY_ABSOLUTE_PATH ?= $(shell pwd)/jwtRS512.key
APIGEE_API_TOKEN ?= $(shell export SSO_LOGIN_URL=https://login.apigee.com && eval get_token -u $(APIGEE_USERNAME))

# set valus in .env. See ReadMe for more details.
export APIGEE_ENVIRONMENT
export SERVICE_BASE_PATH
export FULLY_QUALIFIED_SERVICE_NAME

export CLIENT_ID
export CLIENT_SECRET

export APIGEE_API_TOKEN
export JWT_PRIVATE_KEY_ABSOLUTE_PATH

export OAUTH_BASE_URI=https://$(APIGEE_ENVIRONMENT).api.service.nhs.uk
export OAUTH_PROXY=oauth2
export REDIRECT_URL=https://nhsd-apim-testing-internal-dev.herokuapp.com/callback

run:
	../.venv/bin/pytest -s -v $(f)

# run tests with certain marker e.g. make run-sandbox runs tests marked with sandbox
run-%:
	../.venv/bin/pytest -s -v -m "$*" $(f)