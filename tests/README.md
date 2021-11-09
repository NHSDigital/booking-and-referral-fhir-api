# readme-to-test

A simple README to explain the tests flow.


## Installation

If you didn't follow the instruction on the main [README](../README.md).

Please run:

`make install`
```
Make install will install all the requirements in your local machine that you can use to run some make commands such as:

 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format
```

## Test flow to test new develops
By default this proxy it's pointing to bars mock receiver which is pointing to a docker container as a backend. This backend it's responsible
to manage the requests made through this proxy.

In order to run the tests you need to follow this further configurations:

1. Create a branch on the [Booking and Referral api](https://github.com/NHSDigital/booking-and-referral-fhir-api) repo.

2. After all your changes, please, commit and push them into the repo.

3. Then open [Booking and Referral api](https://github.com/NHSDigital/booking-and-referral-fhir-api) repo UI on Github and raise a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

4. Open a pull request on [bars-mock-receiver-proxy](https://github.com/NHSDigital/bars-mock-receiver-proxy).
5. After both pull request being deployed please follow these steps:
   1. Go to Apigee and find your deploy. must be in: `booking-and-referral-pr-` your PR number from Github on step 4.
   2. Navigate to developer mode and at the bottom change the file `SetTargetUrl.js`.
   3. On this file add the follow line:
      1. `targetUrl = "https://internal-dev.api.service.nhs.uk/bars-mock-receiver-proxy-pr` + your PR number on the mock receiver repo. This value come from the step 4.
   4. After set the targetUrl your current PR on mock receiver, you need to set the other way around. On Apigee open the deploy of your PR but this time on the mock receiver.
   5. Go to develop and click on `bars-mock-receiver-target`. A xml will be presented and you need to edit the element `<Path>/bref-X</Path>` and the X must the number of your PR on the step 3.




To run the tests you need to set a variety of environment variables. One of them has a dependency of an utility from Apigee that must be installed.

Please, follow the further steps to install, [get_token](https://docs.apigee.com/api-platform/system-administration/auth-tools#install).

Install get_token
-----------------------

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

Setup environment variables
-----------------------

Various scripts and commands rely on environment variables being set.

Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

Or consider filling the script ```/test/configuration/env-variables.sh``` Follow the steps described in the script.


Various commands rely on environment variables being defined to set them please fill the `{PLACEHOLDER}` fields in the
 [tests/configuration/env-variables.sh](configuration/env-variables.sh) script.

After complete, the script with your information run it to set the values in your environment.

`sh env-variables.sh`

### Understanding the use of this variables

You can run the test against multiple environments and to manage that you need to set the environment name that you would like to test in the variable `APIGEE_ENVIRONMENT`.

The `APIGEE_ENVIRONMENT` variable will complement a couple others variables to set the target of our tests.

e.g. to set sandbox as a target environment.
```
export APIGEE_ENVIRONMENT='sandbox'
export BASE_URL='https://'$APIGEE_ENVIRONMENT'.api.service.nhs.uk'
export SERVICE_BASE_PATH='booking-and-referral'
export FULLY_QUALIFIED_SERVICE_NAME='booking-and-referral-'$APIGEE_ENVIRONMENT
```

To run the tests against `internal-dev` just update the variable value.
e.g. to set sandbox as a target environment.
```
export APIGEE_ENVIRONMENT='internal-dev'
```

## Command line

How to run the tests.

[Pytest](https://docs.pytest.org/en/6.2.x/) allows us to use [markers](https://docs.pytest.org/en/6.2.x/example/markers.html) to decorate a test method. This way we define the scope of our tests.

e.g. to test our sandbox tests
```
poetry run pytest -m sandbox
```

e.g. to test our ping test
```
poetry run pytest -m ping
```

you can use the marker listed in the [pytest.ini](../pytest.ini)


## TROUBLESHOOTING

 * If the test fail, check the following:

   - Are the environment variables been set?
   - Make sure your detail on the environment variables is the correct ones.
   - Make sure you run the commands to run the test inside the `tests/` folder.
   - Make sure you run the `sh env-variables.sh` with the same shell you run the tests.
