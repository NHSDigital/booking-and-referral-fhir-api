SHELL=/bin/bash -euo pipefail

install-python:
	poetry install

install-node:
	npm install --legacy-peer-deps
	cd sandbox && npm install --legacy-peer-deps

pre-commit-hook:
	source .venv/bin/activate && pre-commit install

install: install-node install-python pre-commit-hook

lint:
	npm run lint
	find . -name '*.py' -not -path '**/.venv/*' -not -path './proxies/sandbox/apiproxy/resources/py/*' | xargs poetry run flake8

clean:
	rm -rf build
	rm -rf dist

publish: clean
	mkdir -p build
	node_modules/.bin/openapi-generator-cli generate -i specification/booking-and-referral.yaml | poetry run python scripts/yaml2json.py | poetry run python scripts/set_version.py > build/booking-and-referral.json
	node_modules/.bin/openapi-generator-cli generate -i specification/booking-and-referral-1.1.0.yaml | poetry run python scripts/yaml2json.py | poetry run python scripts/set_version.py > build/booking-and-referral-1.1.0.json

serve:
	npm run serve

check-licenses:
	npm run check-licenses
	scripts/check_python_licenses.sh

format:
	poetry run black **/*.py

start-sandbox:
	cd sandbox && npm run start

build-proxy:
	scripts/build_proxy.sh

copy-examples:
	cp -r  specification/examples sandbox/src/routes/examples

_dist_include="pytest.ini poetry.lock poetry.toml sandbox pyproject.toml Makefile build/. tests specification terraform infra"

release: clean copy-examples publish build-proxy
	mkdir -p dist
	for f in $(_dist_include); do cp -r $$f dist; done
	cp ecs-proxies-deploy.yml dist/ecs-deploy-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev-sandbox.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-dev.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-int.yml
	cp ecs-proxies-deploy.yml dist/ecs-deploy-internal-qa.yml
