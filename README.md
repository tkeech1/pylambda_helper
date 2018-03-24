[![Build Status](https://travis-ci.org/tkeech1/pylambda_helper.svg?branch=master)](https://travis-ci.org/tkeech1/pylambda_helper)
[![codecov](https://codecov.io/gh/tkeech1/pylambda_helper/branch/master/graph/badge.svg)](https://codecov.io/gh/tkeech1/pylambda_helper)

## Helper for AWS Lambda

1) Run tests in Docker - use any docker image that contains pip3 and python3
```
docker build -t pylambda_helper:latest . 
docker run -it --rm -v ${PWD}:/app pylambda_helper:latest python3 -m pytest
```
-Or-

```
make test-local
```