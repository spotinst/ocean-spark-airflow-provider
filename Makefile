.DEFAULT_GOAL := help

PROJECT_VERSION=1.1.0
SRCS=$(shell git ls-files -c)
DEPS=$(SRCS) pyproject.toml
PROJECT_NAME=ocean-spark-airflow-provider
PACKAGE_NAME=ocean_spark_airflow_provider

Q := $(if $(filter 1,$(V)),,@)

##@ General

.PHONY: help
help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "Usage: make \033[36m<target>\033[0m\n"} /^[a-zA-Z0-9_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

.venv: pyproject.toml poetry.lock
	@echo "[INS] $@"
	poetry install
	touch .venv

pyproject.toml: pyproject.toml.in Makefile
	@echo "[GEN] $@"
	sed -e 's/@PROJECT_VERSION@/$(PROJECT_VERSION)/' \
        -e 's/@PROJECT_NAME@/$(PROJECT_NAME)/' \
		-e 's/@AIRFLOW_DEPS_VERSION@/$(AIRFLOW_DEPS_VERSION)/' \
		-e 's/@AIRFLOW_ENTRY_POINTS@/$(AIRFLOW_ENTRY_POINTS)/' \
		-e 's/@PYTHON_VERSION@/$(PYTHON_VERSION)/' \
        <$< >$@


##@ Development

.PHONY: fmt
fmt: .venv ## Format code with black
	@echo "[FMT]"
	poetry run black ocean_spark tests

.PHONY: check-fmt
check-fmt: .venv ## Check format code with black
	@echo "[CHK] style"
	poetry run black --check ocean_spark tests

.PHONY: check-typing
check-typing: .venv ## Check typing with mypy
	@echo "[CHK] typing"
	poetry run mypy ocean_spark tests

.PHONY: check-linter
check-linter: .venv ## Lint code with flake8
	@echo "[CHK] linting"
	poetry run flake8 ocean_spark tests

.PHONY: test
test: .venv ## Run test with pytest
	@echo "[CHK] unit tests"
	 poetry run pytest

.PHONY: all-tests
all-tests: check-fmt check-typing check-linter test ## Run all tests and checks


##@ Build

SDIST_NAME=$(PROJECT_NAME)-$(PROJECT_VERSION).tar.gz

dist/$(SDIST_NAME): $(DEPS)
	@echo "[BLD] sdist pakcages"
	poetry build  --format sdist

.PHONY: sdist
sdist: dist/$(SDIST_NAME)

BDIST_TRIPLET=py3-none-any
WHEEL_NAME=$(PROJECT_NAME)-$(PROJECT_VERSION)-$(BDIST_TRIPLET).whl

dist/$(WHEEL_NAME): $(DEPS)
	@echo "[BLD] wheel pakcages"
	poetry build  --format wheel

.PHONY: wheel
wheel: dist/$(WHEEL_NAME)

.PHONY: dist
dist: dist/$(WHEEL_NAME) ## Build distribution

.PHONY: build
build: sdist wheel ## Build package

##@ Local deployment

.PHONY: check_docker_compose
check_docker_compose:
	@echo "[CHK] docker-compose"
	if command -v docker-compose >/dev/null 2>&1; then \
		exit 0; \
	else \
		echo 'Install a Docker engine, probably at https://docs.docker.com/install/'; \
		exit 1; \
	fi

.PHONY: serve_airflow
AIRFLOW_PYTHON_VERSION ?=
AIRFLOW_VERSION ?=
serve_airflow: check_docker_compose clean_airflow dist/$(WHEEL_NAME) ## Run airflow locally
	@echo "[RUN] docker-compose up"
	cd deploy/airflow; \
	AIRFLOW_PYTHON_VERSION=$(AIRFLOW_PYTHON_VERSION) AIRFLOW_VERSION=$(AIRFLOW_VERSION) docker-compose -p airflow up --force-recreate --build --remove-orphans

.PHONY: clean_airflow
clean_airflow: ## Clean up all airflow resources
	@echo "[RUN] docker-compose clean"
	rm dist/*; \
	cd deploy/airflow; \
	docker-compose down --volumes --remove-orphans

##@ Publish
.PHONY: publish
publish: dist/$(SDIST_NAME) dist/$(WHEEL_NAME) ## Publish packages
	poetry publish


.PHONY: clean
clean: | clean_airflow
	@echo "[CLN] cleaning repository"
	git clean -dfx

serve_airflow_2_0_2: AIRFLOW_PYTHON_VERSION=3.7
serve_airflow_2_0_2: AIRFLOW_VERSION=2.0.2
serve_airflow_2_0_2: serve_airflow

serve_airflow_2_2_2: AIRFLOW_PYTHON_VERSION=3.7
serve_airflow_2_2_2: AIRFLOW_VERSION=2.2.2
serve_airflow_2_2_2: serve_airflow

serve_airflow_2_4_3: AIRFLOW_PYTHON_VERSION=3.10
serve_airflow_2_4_3: AIRFLOW_VERSION=2.4.3
serve_airflow_2_4_3: serve_airflow

serve_airflow_2_5_1: AIRFLOW_PYTHON_VERSION=3.10
serve_airflow_2_5_1: AIRFLOW_VERSION=2.5.1
serve_airflow_2_5_1: serve_airflow

serve_airflow_2_6_3: AIRFLOW_PYTHON_VERSION=3.10
serve_airflow_2_6_3: AIRFLOW_VERSION=2.6.3
serve_airflow_2_6_3: serve_airflow

serve_airflow_2_7_2: AIRFLOW_PYTHON_VERSION=3.11
serve_airflow_2_7_2: AIRFLOW_VERSION=2.7.2
serve_airflow_2_7_2: serve_airflow

serve_airflow_2_8_1: AIRFLOW_PYTHON_VERSION=3.11
serve_airflow_2_8_1: AIRFLOW_VERSION=2.8.1
serve_airflow_2_8_1: serve_airflow


$(V).SILENT:
