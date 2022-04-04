.SILENT:

ENVIRONMENT=dev

-include .env

TERRAFORM_VARS=-var=\"environment=$(ENVIRONMENT)\" -var=\"aws_account_id=$(aws_account_id)\" -var=\"aws_role_name=$(aws_role_name)\"
AWS_MFA=--mfa=$(aws_role)

#export AWS_SECRET_ACCESS_KEY = $(aws_secret_access_key)
#export AWS_ACCESS_KEY_ID = $(aws_access_key_id)


init:
	AWS_PROFILE=default terraform init -backend-config="key=bars/${ENVIRONMENT}" $(TERRAFORM_VARS)

plan:
	terraform plan

apply:
	 terraform apply
