#* Variables
SHELL := /usr/bin/env bash
PYTHON := python3
OS := $(shell $(PYTHON) -c "import sys; print(sys.platform)")

ifeq ($(OS),win32)
	PYTHONPATH := $(shell $(PYTHON) -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov={{ cookiecutter.package_name }} tests/
else
	PYTHONPATH := `pwd`
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov={{ cookiecutter.package_name }} tests/
endif

#* Docker variables
IMAGE := {{ cookiecutter.package_name }}
VERSION := latest

.PHONY: lock install {% if cookiecutter.install_pre_commit %}pre-commit-install{% endif %} polish-codestyle formatting test check-codestyle lint doc-build doc-serve docker-build docker-remove cleanup help

help:
	@echo "lock                                      Lock the dependencies."
	@echo "install                                   Install the project dependencies."
{%- if cookiecutter.install_pre_commit %}
	@echo "pre-commit-install                        Install the pre-commit hooks."
{%- endif %}
	@echo "polish-codestyle                          Format the codebase."
	@echo "formatting                                Format the codebase."
	@echo "test                                      Run the tests."
	@echo "check-codestyle                           Check the codebase for style issues."
	@echo "lint                                      Run the tests and check the codebase for style issues."
	@echo "doc-build                                 Build docs."
	@echo "doc-serve                                 Build and serve docs."
	@echo "docker-build                              Build the docker image."
	@echo "docker-remove                             Remove the docker image."
	@echo "cleanup                                   Clean the project directory."
	@echo "help                                      Display this help message."


lock:
	poetry lock -n && poetry config warnings.export false && poetry export -f requirements.txt --output requirements.txt

install: lock
	poetry install -n

{%- if cookiecutter.install_pre_commit %}
pre-commit-install:
	poetry run pre-commit install
{%- endif %}

polish-codestyle:
	poetry run ruff format --config pyproject.toml .
	poetry run ruff check --fix --config pyproject.toml .

formatting: polish-codestyle
format: polish-codestyle

test:
	$(TEST_COMMAND)
	poetry run coverage-badge -o assets/images/coverage.svg -f

check-codestyle:
	poetry run ruff format --check --config pyproject.toml .
	poetry run ruff check --config pyproject.toml .
{%- if cookiecutter.install_darglint %}
	poetry run darglint --verbosity 2 {{ cookiecutter.package_name }} tests
{%- endif %}

{% if cookiecutter.install_safety -%} 
check-safety:
	poetry check
	poetry run safety check --full-report --ignore 51457
	poetry run bandit -ll --recursive {{ cookiecutter.package_name }} tests
{%- endif %} 

lint: test check-codestyle {% if cookiecutter.install_safety %}check-safety{% endif %}


doc-build:
	mkdocs build

doc-serve: doc-build
	mkdocs serve

# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION={{ cookiecutter.version }}
docker-build:
	@echo Building docker $(IMAGE):$(VERSION) ...
	docker build \
		-t $(IMAGE):$(VERSION) . \
		-f ./docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION={{ cookiecutter.version }}
docker-remove:
	@echo Removing docker $(IMAGE):$(VERSION) ...
	docker rmi -f $(IMAGE):$(VERSION)

cleanup:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	find . | grep -E ".DS_Store" | xargs rm -rf
	find . | grep -E ".mypy_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	rm -rf build/
