

all: build run

images:
	docker images | grep sloats

ps:
	docker ps -a | grep sloats

build:
	docker build -t sloats/flask-iss:latest .

run:
	docker run --name "flask-iss" -d -p 5016:5000 sloats/flask-iss:latest

push:
	docker push sloats/flask-iss-position-and-sightings:latest
