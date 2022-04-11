.SILENT:

environment = dev
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

destroy: workspace
	AWS_PROFILE=$(aws_profile) terraform destroy

# Docker - lambda
docker-build:
	cp -r ../specification/examples ../mock-receiver
	docker build --platform linux/amd64 -t mock-receiver-$(environment):latest -f ../mock-receiver/Dockerfile ../mock-receiver

docker-tag: docker-build
	docker tag mock-receiver-$(environment):latest $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com/bars-mock-receiver-$(environment)-ecr-repo:latest

docker-login:
	aws ecr get-login-password --profile $(aws_profile) --region eu-west-2 | docker login --username AWS --password-stdin $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com

docker-push: docker-tag docker-login
	docker push $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com/bars-mock-receiver-$(environment)-ecr-repo:latest

test:
	curl -X GET --key client.key --cert truststore.crt -i https://$(environment).bars.dev.api.platform.nhs.uk/mock-receiver/Appointment

clean:
	rm -rf build .terraform upload-key
