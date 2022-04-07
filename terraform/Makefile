.SILENT:

ENVIRONMENT=dev
aws_profile = apim-dev

-include .env

init:
	AWS_PROFILE=$(aws_profile) terraform init -backend-config="key=bars/${ENVIRONMENT}" $(TERRAFORM_VARS)

plan:
	AWS_PROFILE=$(aws_profile) terraform plan

apply:
	AWS_PROFILE=$(aws_profile) terraform apply -auto-approve

destroy:
	AWS_PROFILE=$(aws_profile) terraform destroy

docker-build:
	cp -r ../specification/examples ../mock-receiver
	docker build --platform linux/amd64 -t mock-receiver-$(ENVIRONMENT):latest -f ../mock-receiver/Dockerfile ../mock-receiver

docker-tag: docker-build
	docker tag mock-receiver-$(ENVIRONMENT):latest $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com/bars-mock-receiver-$(ENVIRONMENT)-ecr-repo:latest

docker-login:
	aws ecr get-login-password --profile $(aws_profile) --region eu-west-2 | docker login --username AWS --password-stdin $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com

docker-push: docker-tag docker-login
	docker push $(aws_account_no).dkr.ecr.eu-west-2.amazonaws.com/bars-mock-receiver-$(ENVIRONMENT)-ecr-repo:latest


clean:
	rm -rf build .terraform
