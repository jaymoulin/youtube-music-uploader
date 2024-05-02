.PHONY: all test publish install clean check build-docker publish-docker

VERSION ?= 1.2.0
CACHE ?= --no-cache=1

all: build-docker publish-docker
build-docker:
	docker buildx build --platform linux/arm/v7,linux/arm64/v8,linux/amd64 ${PUSH} --build-arg VERSION=${VERSION} --tag jaymoulin/youtube-music-uploader --tag jaymoulin/youtube-music-uploader:${VERSION} ${CACHE} -f ./docker/Dockerfile .
publish-docker:
	PUSH=--push CACHE= make build-docker


test: install
	twine upload -r testpypi dist/*
publish: install
	twine upload dist/*
install: clean check
	sudo python3 setup.py sdist
check:
	python3 setup.py check --restructuredtext
build:
	mkdir -p build
dist:
	mkdir -p dist
clean: build dist
	sudo rm -Rf build/*
	sudo rm -Rf dist/*
