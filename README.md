## Helper for AWS Lambda

1) Run tests in Docker - use any docker image that contains pip3 and python3
```
docker run -it --rm -v <PATH_TO_SOURCE>:/app <DOCKER_IMAGE> /bin/bash -c 'pip3 install -r requirements.txt && python3 -m pytest'
```
