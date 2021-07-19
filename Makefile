#!/usr/bin/env make

NAME=terraform-operator
TAG?=$(shell git describe --tags --always)

CI_REGISTRY_IMAGE?=retr0h/$(NAME)
CONTAINER=$(CI_REGISTRY_IMAGE):$(TAG)
CONTAINER_LATEST=$(CI_REGISTRY_IMAGE):latest

.PHONY: run
run:
	poetry run kopf run terraform_operator/handlers.py --verbose

.PHONY: build
build: image-build image-tag

.PHONY: image-build
image-build:
	@docker build -t $(CONTAINER) .

.PHONY: image-tag
image-tag:
	@docker tag $(CONTAINER) $(CONTAINER_LATEST)

.PHONY: dep
dep:
	pip install poetry
	poetry install

.PHONY: test
test: lint format-check unit

.PHONY: lint
lint:
	poetry run flake8
	docker run --rm -i hadolint/hadolint < Dockerfile

.PHONY: format-check
format-check:
	poetry run black --diff --check .
	poetry run isort --check-only --diff .

.PHONY: format
format:
	poetry run black .
	poetry run isort .

.PHONY: unit
unit:
	poetry run py.test
