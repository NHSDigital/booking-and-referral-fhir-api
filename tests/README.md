# readme-to-test

A simple README to explain the tests flow.


## Installation

If you didn't follow the instruction on the main [README](../README.md).

Please run:

`make install` from the root of this project
```
Make install will install all the requirements in your local machine that you can use to run some make commands such as:

 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format
```

## Test flow to test new develops
When testing we mock the reciever. Our AWS mock reciever is under this folder `/terraform/mock-receiver`
Our mock-receiver runs a fargate container which is inside the AWS is responsible for managing the requests made through this proxy.
The code for container can be found in this repo under `/sandbox`.

If you have made code changes to  `/sandbox` in your PR and wish to point your PR tests towards this backend you will need to follow the below steps:

### Open Pull requests
1. Create a branch on the [Booking and Referral fhir api](https://github.com/NHSDigital/booking-and-referral-fhir-api) repo.

2. After all your changes, please, commit and push them into the repo.

3. Then open [Booking and Referral fhir api](https://github.com/NHSDigital/booking-and-referral-fhir-api) repo UI on Github and raise a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

4. Create a new identifier inside targets.json file in the [booking-and-referral-targets](https://github.com/NHSDigital/booking-and-referral-targets/blob/master/targets/internal-dev/targets.json) (e.g:"NHS0001": "https://{environment}.bars.dev.api.platform.nhs.uk" )

5. Now follow the instructions in the [terraform readme](/terraform/README.md) to deploy your AWS environment and include  your shortname in the .env file.

After both pull request have been deployed in apigee please follow part 2.

## Set up to run tests

Install get_token
-----------------------
The APIGEE_TOKEN env variable has a a dependency of an utility from Apigee that must be installed.

To install acurl and get_token:

1. Create an install directory on your machine or use the default usr/local/bin directory.
2. Download the installation ZIP file from Apigee:

`curl https://login.apigee.com/resources/scripts/sso-cli/ssocli-bundle.zip -O`

3. Unzip the downloaded file.
4. Execute the install script:

`sudo ./install -b /usr/local/bin`

<sub>The -b option specifies the location of the executable files. If you do not specify this option, the install script installs the utilities in /usr/local/bin.<sub>

5. Test the installations:

 `   acurl -h
    get_token -h`


If the install is successful, these commands return Help text for the utilities.

More info can be found at [get_token](https://docs.apigee.com/api-platform/system-administration/auth-tools#install).

Setup environment variables
-----------------------

Various scripts and commands rely on environment variables being set.

Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

Variables you will require
- `APIGEE_ENVIRONMENT` e.g. internal-dev
- `APIGEE_USERNAME` - your username

- `FULLY_QUALIFIED_SERVICE_NAME=booking-and-referral-$(APIGEE_ENVIRONMENT)`
- `SERVICE_BASE_PATH=booking-and-referral/FHIR/R4`
- `CLIENT_ID` and `CLIENT_SECRET`  are only required for int. Otherwise use dummy value
- you will also require the correct jwt private key file.

If running tests against a deployed PR on internal-dev or internal-dev-sandbox environments `FULLY_QUALIFIED_SERVICE_NAME` and `SERVICE_BASE_PATH` will be as follows:

For internal-dev:
- `FULLY_QUALIFIED_SERVICE_NAME=booking-and-referral-pr-$(PR_NO)` e.g. booking-and-referral-pr-92
- `SERVICE_BASE_PATH=booking-and-referral/FHIR/R4-pr-$(PR_NO)` e.g. booking-and-referral/FHIR/R4-pr-92

Or for internal-dev-sandbox
- `FULLY_QUALIFIED_SERVICE_NAME=booking-and-referral-pr-$(PR_NO)-sandbox` e.g. booking-and-referral-pr-92-sandbox
- `SERVICE_BASE_PATH=booking-and-referral/FHIR/R4-pr-$(PR_NO)` e.g. booking-and-referral/FHIR/R4-pr-92



Once variables have been defined in your .env file
- You can fill the script ```/test/configuration/env-variables.sh``` . Follow the steps described in the script to set all env variables. Then you can run tests.

- OR Use the Makefile targets to run tests. The `make run` targets will set the env variables before running tests.

### Understanding the use of this variables

You can run the test against multiple environments and to manage that you need to set the environment name that you would like to test in the variable `APIGEE_ENVIRONMENT`.

The `APIGEE_ENVIRONMENT` variable will complement a couple others variables to set the target of our tests.

e.g. to set sandbox as a target environment.
```
export APIGEE_ENVIRONMENT='sandbox'
export BASE_URL='https://'$APIGEE_ENVIRONMENT'.api.service.nhs.uk'
export SERVICE_BASE_PATH='booking-and-referral/FHIR/R4'
export FULLY_QUALIFIED_SERVICE_NAME='booking-and-referral-'$APIGEE_ENVIRONMENT
```

To run the tests against `internal-dev` just update the variable value.
e.g. to set sandbox as a target environment.
```
export APIGEE_ENVIRONMENT='internal-dev'
```

## Command line

How to run the tests.
You can use the make targets defined in Makefile

To run all tests
```
make run
```

To run a certain file of tests
```
make run f=test_appointment.py
```

To run one test
```
make run f=test_appointment.py::TestAppointment::test_get_appointment
```

[Pytest](https://docs.pytest.org/en/6.2.x/) allows us to use [markers](https://docs.pytest.org/en/6.2.x/example/markers.html) to decorate a test method. This way we define the scope of our tests.

e.g. to test our sandbox tests
```
make run-sandbox
```

e.g. to test our ping test
```
make run-ping
```

you can use the marker listed in the [pytest.ini](../pytest.ini)


## TROUBLESHOOTING

 * If the test fail, check the following:

   - Are the environment variables been set?
   - Make sure your detail on the environment variables is the correct ones.
   - Make sure you run the commands to run the test inside the `tests/` folder.
