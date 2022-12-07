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
$ cd terraform
$ terraform init
```
```
$ terraform plan
```
This will prompt you to enter a region, e.g. "eu-west-2"
```
$ terraform apply
```
This may ask you for confirmation before execution.

## Implementation
This repository contains two directory that together create mock-receiver service. The first directory is called `infra`. This
folder contains all the configuration related to the networking and infrastructure. You probably don't need to either change
or redeploy contents of this directory.

The second directory is `terraform` directory and the content of this directory is the mock-service itself.
It contains a few modules of which the most important one is `mock-receiver`. This module contains the configuration of the
container that will be deployed to the cluster. When you `terraform apply`, it builds the `mock-reciever` directory as a 
container and push the image to the ECR. Then it runs the uploaded image inside a fargate environment. 

### per-user and per-pr environment
You can create your own deployment locally. This works similar to PR deployment that we have in other repositories, but 
the difference is that you can run it locally with your own prefixed name. Our convention is to use our NHS short username
as environment prefix.
Create a `.env` file and set `environment=<short-username>`. When you run `terraform apply` you should see all services
are prefixed with your short username. Now you can start making changes and keep redeploying until you are happy with 
your changes.

### internal environments deployment
Once you are happy with your changes you need to re-deploy your changes to the `dev` environment. In AWS we only have one 
development environment and, it's called `dev`. All apigee internal environments will use this `dev` environment as their 
backend i.e. mock-receiver. *You need to deploy to `dev` environment manually, since we don't have pipeline integration.*

### Troubleshooting
When you make changes and deploy mock-receiver, fargate won't restart the service automatically, or it takes long time to 
do so. mock-receiver is a test service so uptime is not an issue. You can login into your AWS account and select the appropriate 
service (the one with your short username or dev) and delete all services. Fargate will launch new instances in a few seconds,
and because you just pushed new changes to the ECR image this time it will pick up the latest version of the image. 

