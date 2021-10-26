SHELL=/bin/bash -euo pipefail

install-python:
	poetry install

install-node:
	npm install
	cd sandbox && npm install

pre-commit-hook:
	cp scripts/pre-commit .git/hooks/pre-commit

install: install-node install-python pre-commit-hook

test:
#	this target should be used for local unit tests ..  runs as part of the build pipeline
	make --no-print-directory -C sandbox test

sandbox-test:
	poetry run pytest -m sandbox

smoketest:
#	this target is for end to end smoketests this would be run 'post deploy' to verify an environment is working
	poetry run pytest -v --junitxml=smoketest-report.xml -s -m smoketest
