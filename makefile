

build:
	docker build -t test .

run: build
	docker run --rm --name aws-route53-dynamicip -it test