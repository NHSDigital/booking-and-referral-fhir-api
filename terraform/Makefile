.SILENT:

aws_profile = apim-dev
tr_vars=
tr_cmd = AWS_PROFILE=$(aws_profile) terraform

-include .env

workspace:
	$(tr_cmd) workspace new $(environment) || $(tr_cmd) workspace select $(environment) && echo "Switched to workspace/environment: $(environment)"

init:
	$(tr_cmd) init -backend-config="key=bars" $(tr_vars)

plan: workspace
	$(tr_cmd) plan

apply: workspace
	$(tr_cmd) apply -auto-approve

destroy:
	$(tr_cmd) destroy $(tr_vars)

test:
	curl -X GET --key client.key --cert client.crt -i https://$(environment).bars.dev.api.platform.nhs.uk/Appointment

clean:
	rm -rf build .terraform upload-key

mock_receiver_repository_name = bars-mock-receiver-$(environment)
mock_receiver_repository_url = $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com/$(mock_receiver_repository_name)

docker-login:
	aws ecr get-login-password --profile $(aws_profile) --region eu-west-2 | docker login --username AWS --password-stdin $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com

docker-build-sandbox:
	cp -r ../specification/examples ../sandbox/src/routes
	docker build --platform linux/amd64 -t $(mock_receiver_repository_name):latest -f ../sandbox/Dockerfile ../sandbox

docker-tag-sandbox: docker-build-sandbox
	docker tag $(mock_receiver_repository_name):latest $(mock_receiver_repository_url):latest

docker-push-sandbox: docker-tag-sandbox docker-login
	docker push $(mock_receiver_repository_url):latest
