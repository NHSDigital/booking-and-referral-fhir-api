# Building infrastructure with Terraform (using AWS CLI)

## Prerequisites

1. [Terraform CLI](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started) installed
2. [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) installed 
3. Your AWS credentials. (Create an access key for your user account)
4. Set up you AWS account for AWS CLI usage (https://nhsd-confluence.digital.nhs.uk/pages/viewpage.action?spaceKey=APM&title=KOP-011+Set+up+AWS+Account+for+CLI+Usage)

### Step 1

Configure the AWS CLI from your terminal by inputing your AWS Access Key ID and Secret Access Key using the following command:
```
$ aws configure
```
Once configured, your credentials will be stored in a file at `~/.aws/credentials`.

### Step 2

Follow the instructions [here](https://nhsd-confluence.digital.nhs.uk/pages/viewpage.action?spaceKey=APM&title=KOP-011+Set+up+AWS+Account+for+CLI+Usage), once aws_mfa_update has been setup run this command to get a new token:
```
$ aws-mfa-update 347250048819 <your aws name> <aws mfa code>
```
The result of this step should be a working aws_mfa_update script and a `~/.aws/config` file containing the Role you will assume (NHSDAdminRole).

### Step 3

Set AWS_PROFILE to the role you will assume, e.g.
```
$ export AWS_PROFILE=NHSDAdminRole
```

### Step 4

Run Terraform using the following:
```
$ terraform init
```
```
$ terraform plan
```
```
$ terraform apply
```
This may ask you for confirmation before execution.
