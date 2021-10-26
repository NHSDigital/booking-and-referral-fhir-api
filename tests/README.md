# readme-to-test

A simple README to explain the tests flow.

## Installation

If you didn't follow the instruction on the main [README](../README.md).

Please run:

`make install`

Various commands rely on environment variables being set. In order to set them please fill the `{placeholders}` in the
 [tests/configuration/env-variables.sh](configuration/env-variables.sh) script.

After complete, the script with your information run it to set the values in your environment.

`sh env-variables.sh`


## Command line

The tests can be triggered by executing the following command in the target project's tests directory:

```
make sandbox-test
```

## TROUBLESHOOTING

 * If the test fail, check the following:

   - Are the environment variables been set?

   - Make sure your detail on the environment variables is the correct ones.
