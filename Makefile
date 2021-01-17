.PHONY: all test publish install clean check build-docker publish-docker latest

VERSION ?= 1.1.0
CACHE ?= --no-cache=1
FULLVERSION ?= 1.6.3
archs ?= amd64 i386 arm64v8 arm32v6
all: build-docker publish-docker latest
qemu-arm-static:
	cp /usr/bin/qemu-arm-static .
qemu-aarch64-static:
	cp /usr/bin/qemu-aarch64-static .
build-docker: qemu-arm-static qemu-aarch64-static
	$(foreach arch,$(archs), \
		cat docker/Dockerfile | sed "s/FROM python:alpine/FROM ${arch}\/python:alpine/g" > .Dockerfile; \
		docker build -t jaymoulin/youtube-music-uploader:${VERSION}-$(arch) -f .Dockerfile --build-arg VERSION=${VERSION} ${CACHE} .;\
	)
publish-docker:
	docker push jaymoulin/youtube-music-uploader
	cat docker/manifest.yml | sed "s/\$$VERSION/${VERSION}/g" > manifest.yaml
	cat manifest.yaml | sed "s/\$$FULLVERSION/${FULLVERSION}/g" > manifest2.yaml
	mv manifest2.yaml manifest.yaml
	manifest-tool push from-spec manifest.yaml
latest: build-docker
	FULLVERSION=latest VERSION=${VERSION} make publish-docker
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
