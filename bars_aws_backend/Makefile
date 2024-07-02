build:
	docker build -t bars-lambda-build -f lambda.Dockerfile .

package: build
	mkdir -p build
	docker run --rm -v $(shell pwd)/build:/build bars-lambda-build

test:
	python -m unittest

.PHONY: build package test