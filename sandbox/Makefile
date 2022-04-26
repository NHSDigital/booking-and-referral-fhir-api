copy-examples:
	cp -r ../specification/examples src/routes

docker-build: copy-examples
	docker build -t bars-sandbox .

docker-run:
	docker run -it -p 9000:9000 bars-sandbox
