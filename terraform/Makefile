.SILENT:

ENVIRONMENT=dev

-include .env

TERRAFORM_VARS=-var=\"environment=$(ENVIRONMENT)\"

export AWS_SECRET_ACCESS_KEY = $(aws_secret_access_key)
export AWS_ACCESS_KEY_ID = $(aws_access_key_id)

init:
	terraform init -backend-config="key=bars/${ENVIRONMENT}" $(TERRAFORM_VARS)

plan:
	terraform plan

apply:
	 terraform apply -auto-approve

all: plan apply
