.DEFAULT_GOAL := all
isort = isort pydantic tests
black = black -S -l 120 --target-version py38 pydantic tests

.PHONY: install-linting
install-linting:
	pip install -r tests/requirements-linting.txt

.PHONY: install-esridumpgdf
install-pydantic:
	python -m pip install -U wheel pip
	pip install -r requirements.txt
	pip install -e .

.PHONY: install-testing
install-testing: install-pydantic
	pip install -r tests/requirements-testing.txt

.PHONY: install
install: install-testing install-linting install-docs
	@echo 'installed development requirements'

.PHONY: build
build:
	python setup.py build_ext --inplace

.PHONY: format
format:
	$(isort)
	$(black)

.PHONY: lint
lint:
	flake8 pydantic/ tests/
	$(isort) --check-only --df
	$(black) --check --diff

.PHONY: check-dist
check-dist:
	python setup.py check -ms
	SKIP_CYTHON=1 python setup.py sdist
	twine check dist/*

.PHONY: test
test:
	pytest

.PHONY: all
all: lint

.PHONY: docs
docs:
	flake8 --max-line-length=80 docs/examples/
	python docs/build/main.py
	mkdocs build

.PHONY: docs-serve
docs-serve:
	python docs/build/main.py
	mkdocs serve
