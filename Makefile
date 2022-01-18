.DEFAULT_GOAL := help

PROJECT_VERSION=0.0.1
SRCS=$(shell git ls-files -c)
DEPS=$(SRCS) pyproject.toml
PROJECT_NAME=ocean-spark-airflow-provider
PACKAGE_NAME=ocean_spark_airflow_provider


ifeq ($(V),)
V := 0
endif
Q := $(if $(filter 1,$(V)),,@)


##@ General

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

poetry.lock: pyproject.toml
	@echo "[GEN] $@"
	$(Q)poetry lock

.venv: poetry.lock
	@echo "[INS] $@"
	$(Q)poetry install
	$(Q)touch .venv

pyproject.toml: pyproject.toml.in Makefile
	@echo "[GEN] $@"
	$(Q)sed -e 's/@PROJECT_VERSION@/$(PROJECT_VERSION)/' \
        -e 's/@PROJECT_NAME@/$(PROJECT_NAME)/' \
		-e 's/@AIRFLOW_DEPS_VERSION@/$(AIRFLOW_DEPS_VERSION)/' \
		-e 's/@AIRFLOW_ENTRY_POINTS@/$(AIRFLOW_ENTRY_POINTS)/' \
		-e 's/@PYTHON_VERSION@/$(PYTHON_VERSION)/' \
        <$< >$@


##@ Development

.PHONY: fmt
fmt: .venv ## Format code with black
	@echo "[FMT]"
	$(Q)poetry run black ocean_spark tests

.PHONY: check-fmt
check-fmt: .venv ## Check format code with black
	@echo "[CHK] style"
	$(Q)poetry run black --check ocean_spark tests

.PHONY: check-typing
check-typing: .venv ## Check typing with mypy
	@echo "[CHK] typing"
	$(Q)poetry run mypy ocean_spark tests

.PHONY: check-linter
check-linter: .venv ## Lint code with flake8
	@echo "[CHK] linting"
	$(Q)poetry run flake8 ocean_spark tests

.PHONY: test
test: .venv ## Run test with pytest
	@echo "[CHK] unit tests"
	 $(Q)poetry run pytest

.PHONY: all-tests
all-tests: check-fmt check-typing check-linter test ## Run all tests and checks


##@ Build

SDIST_NAME=$(PROJECT_NAME)-$(PROJECT-VERSION).tar.gz

dist/$(SDIST_NAME): $(DEPS)
	@echo "[BLD] sdist pakcages"
	$(Q)poetry build  --format sdist

BDIST_TRIPLET=py3-none-any
WHEEL_NAME=$(PROJECT_NAME)-$(PROJECT_VERSION)-$(BDIST_TRIPLET).whl

dist/$(WHEEL_NAME): $(DEPS)
	@echo "[BLD] wheel pakcages"
	$(Q)poetry build  --format wheel

.PHONY: wheel
wheel: dist/$(WHEEL_NAME)

.PHONY: build 
build: sdist wheel


build_airflow1:
	TARGET_AIRFLOW_VERSION=1 make build

build_airflow2:
	TARGET_AIRFLOW_VERSION=2 make build

##@ Local deployment 

.PHONY: check_docker_compose
check_docker_compose: 
	@echo "[CHK] docker-compose"
	$(Q)if command -v docker-compose >/dev/null 2>&1; then \
		exit 0; \
	else \
		echo 'Install a Docker engine, probably at https://docs.docker.com/install/'; \
		exit 1; \
	fi

.PHONY: serve_airflow1
serve_airflow1: dist/$(WHEEL_NAME) check_docker_compose
	@echo "[RUN] docker-compose up"
	$(Q)cd deploy/airflow1; \
	docker-compose -p airflow1 up --force-recreate --build --remove-orphans

.PHONY: serve_airflow2
serve_airflow2: dist/$(WHEEL_NAME) check_docker_compose
	@echo "[RUN] docker-compose up"
	$(Q)cd deploy/airflow2; \
	docker-compose -p airflow2 up --force-recreate --build --remove-orphans

.PHONY: clean_airflow
clean_airflow:
	@echo "[RUN] docker-compose clean"
	$(Q)cd deploy/airflow1; \
	docker-compose down --volumes --remove-orphans
	$(Q)cd deploy/airflow2; \
	docker-compose down --volumes --remove-orphans


.PHONY: clean
clean: | clean_airflow
	@echo "[CLN] cleaning repository"
	$(Q)git clean -dfx

$(V).SILENT:
