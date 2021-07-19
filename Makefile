NAME=terraform-operator
TAG?=$(shell git describe --tags --always)

CI_REGISTRY_IMAGE?=retr0h/$(NAME)
CONTAINER=$(CI_REGISTRY_IMAGE):$(TAG)
CONTAINER_LATEST=$(CI_REGISTRY_IMAGE):latest

.PHONY: build
build: image-build image-tag

.PHONY: image-build
image-build:
	@docker build -t $(CONTAINER) .

.PHONY: image-tag
image-tag:
	@docker tag $(CONTAINER) $(CONTAINER_LATEST)
