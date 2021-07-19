# This is a multi-stage build which requires Docker 17.05 or higher.

FROM python:3.8.5-slim-buster as base

ENV APP_NAME=terraform-operator
ENV APP_SRC_DIR=/usr/src/${APP_NAME}
ENV APP_SRC_DIST_DIR=${APP_SRC_DIR}/dist

RUN apt-get update -y

FROM base as terraform-builder

ARG TERRAFORM_VERSION=1.0.2

RUN apt-get install -y curl unzip
RUN curl -sL https://releases.hashicorp.com/terraform/${TERRAFORM_VERSION}/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -o /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip
RUN unzip /tmp/terraform_${TERRAFORM_VERSION}_linux_amd64.zip -d /usr/local/bin

FROM base as terraform-operator-builder

WORKDIR ${APP_SRC_DIR}

ENV PACKAGES="\
    "

RUN apt-get install -y ${PACKAGES}

RUN pip3 install -U pip poetry
ADD terraform-operator .
RUN poetry build

FROM base
LABEL maintainer="נυαη נυαηѕση <@retr0h>"

ENV APP_DIR=/app
ENV PACKAGES="\
    "
ENV BUILD_DEPS="\
    "

WORKDIR ${APP_DIR}

COPY --from=terraform-builder /usr/local/bin/terraform /usr/local/bin/terraform
COPY --from=terraform-operator-builder ${APP_SRC_DIST_DIR} ${APP_SRC_DIST_DIR}

RUN apt-get install ${BUILD_DEPS} ${PACKAGES} \
    && pip3 install -f ${APP_SRC_DIST_DIR} ${APP_NAME} \
    && apt-get remove -y ${BUILD_DEPS} \
    && rm -rf /var/lib/apt/lists/*
