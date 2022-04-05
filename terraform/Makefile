.SILENT:

ENVIRONMENT=dev

-include .env

TERRAFORM_VARS=-var=\"environment=$(ENVIRONMENT)\" -var=\"aws_account_id=$(aws_account_id)\" -var=\"aws_role_name=$(aws_role_name)\"

init:
	AWS_PROFILE=apim-dev terraform init -backend-config="key=bars/${ENVIRONMENT}" $(TERRAFORM_VARS)

plan:
	AWS_PROFILE=apim-dev terraform plan

apply:
	AWS_PROFILE=apim-dev terraform apply

destroy:
	AWS_PROFILE=apim-dev terraform destroy
