SERVICE_NAME = booking-and-referral
PROXY_BASE_PATH = booking-and-referral/FHIR/R4

-include .env

run:
	poetry run pytest -s -v $(cmd_opts)

run-%:
	poetry run pytest -s -m $(subst run-,,$@) -v $(cmd_opts)

