# Booking and Referral FHIR API

![Build](https://github.com/NHSDigital/booking-and-referral-fhir-api/workflows/Build/badge.svg?branch=master)

The bookings and service requests API is defining a standard API for booking of appointments and management of service requests (referrals) between organisations.

This is a RESTful HL7® FHIR® API specification for the *Booking and Referral API*.

* `specification/` This [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers.
* `sandbox/` This Python application implements a mock implementation of the service. Use it as a back-end service to the interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
* `scripts/` Utilities helpful to developers of this specification.
* `proxies/` Live (connecting to another service) and sandbox (using the sandbox container) Apigee API Proxy definitions.

Consumers of the API will find developer documentation on the [NHS Digital Developer Hub](https://digital.nhs.uk/developer/api-catalogue/booking-and-referral-fhir).

## Table of Contents
1. [Contributing](#Contributing)
2. [Development](#Development)
3. [Caveats](#Caveats)


## Contributing
Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](https://github.com/NHSDigital/booking-and-referral-fhir-api/blob/master/CONTRIBUTING.md) and the [community code of conduct](https://github.com/NHSDigital/booking-and-referral-fhir-api/blob/master/CODE_OF_CONDUCT.md).

### Licensing
This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

## Development

### Requirements
* make
* nodejs + npm/yarn
* [poetry](https://github.com/python-poetry/poetry)

### Install
```
$ make install
```

#### Updating hooks
You can install some pre-commit hooks to ensure you can't commit invalid spec changes by accident. These are also run
in CI, but it's useful to run them locally too.

```
$ make pre-commit-hook
```

### Terraform Deployment
Booking and Referrals Service internal deployment depends on mock services. These mock-services are only used for testing
and are not part of the production. Check the readme file in `terraform` directory for more details.


### Environment Variables
Various scripts and commands rely on environment variables being set. These are documented with the commands.

:bulb: Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

### Make commands

There are `make` commands that alias some of this functionality:

Make sure you have run `make install` [here](###Install).

 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format

### Testing
Each API and team is unique. We encourage you to set our test environment in you local machine to run the tests.

Please, check [readme-to-test](/tests/README.md) file.

### VS Code Plugins

 * [openapi-lint](https://marketplace.visualstudio.com/items?itemName=mermade.openapi-lint) resolves links and validates entire spec with the 'OpenAPI Resolve and Validate' command
 * [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) provides sidebar navigation


### Emacs Plugins

 * [**openapi-yaml-mode**](https://github.com/esc-emacs/openapi-yaml-mode) provides syntax highlighting, completion, and path help

### Speccy

> [Speccy](https://github.com/wework/speccy) *A handy toolkit for OpenAPI, with a linter to enforce quality rules, documentation rendering, and resolution.*

Speccy does the lifting for the following npm scripts:

 * `test` -- Lints the definition
 * `publish` -- Outputs the specification as a **single file** into the `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format

(Workflow detailed in a [post](https://developerjack.com/blog/2018/maintaining-large-design-first-api-specs/) on the *developerjack* blog.)

:bulb: The `publish` command is useful when uploading to Apigee which requires the spec as a single file.

### Caveats

#### Swagger UI
Swagger UI unfortunately doesn't correctly render `$ref`s in examples, so use `speccy serve` instead.

#### Apigee Portal
The Apigee portal will not automatically pull examples from schemas, you must specify them manually.

### Platform setup

Successful deployment of the API Proxy requires:

 1. A *Target Server* named `booking-and-referral-target`
 2. A *Key-Value Map* named `bref-variables`, containing any values you might need at proxy runtime
 3. A *Key-Value Map* named `bref-variables-encrypted`, containing any secrets you might need at proxy runtime

The Key-Value maps need to be specifed within the [api-management-infrasture](https://github.com/NHSDigital/api-management-infrastructure) repository to be able to be used with the API proxy.

:bulb: For Sandbox-running environments (`test`) these need to be present for successful deployment but can be set to empty/dummy values.

## Aditional notes
The build pipeline uses Redoc so to find any errors you can use the command below, there are currently loads of warnings which isnt ideal but can be ignored.

```
npx redocly lint --max-problems 300 --skip-rule=security-defined specification/booking-and-referral-1.2.0.yaml
```

To get a single spec file you can use `speccy publish` as above or redoc thus

```
npx redocly  bundle specification/booking-and-referral-1.2.0.yaml --remove-unused-components --ext json -o build/booking-and-referral-1.2.2.json
```

you can then use that file here [swagger.io](https://editor.swagger.io/) to view and see any errors, alternatively you can get access to the Apigee non-prod account, use the form here [SNOW form](https://www.support.internalservices.england.nhs.uk/nhs_digital?id=sc_cat_item&sys_id=440a1c211be0561078ac4337b04bcb5d&sysparm_category=7496f0c81b1c9610772fa756b04bcbf7) to get access, then the portal for [Apigee](https://login.apigee.com/login) Once youve signed in you can click on the `specs` button and upload the specification file, any errors will show at the top.

### Sandbox
see the readme in the sanbox folder.

### Path to live
After you've done any update and got the merged in Master (afer a PR) the build process will kick off in the background and deploy the Sandbox ineternal-dev internal-qa and the INT versions of the changes to Apigee, this can take upto 15 mins. to change the spec file and update the [BloomRech spec page](https://digital.nhs.uk/developer/api-catalogue/booking-and-referral-fhir) you need to post a request the the Slack channel `platforms-apim-producer-support` with a link to the approved PR, a copy of all three Api Spec files (Do not use the partial ones from the repo, use the ones created by the Azure pipline or the ones from redoc)
After this someone will pick up the request and (assuming no errors) make the update for you, once applied this can take upto an hour to show.

