test-local:
	docker build -t pylambda_helper:latest . 
	docker run -it --rm -v ${PWD}:/app pylambda_helper:latest python3 -m pytest