.SILENT:

ENVIRONMENT=dev

-include .env

init:
	AWS_PROFILE=apim-dev terraform init -backend-config="key=bars/${ENVIRONMENT}" $(TERRAFORM_VARS)

plan:
	AWS_PROFILE=apim-dev terraform plan

apply:
	AWS_PROFILE=apim-dev terraform apply -auto-approve

destroy:
	AWS_PROFILE=apim-dev terraform destroy
