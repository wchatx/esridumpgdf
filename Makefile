SHELL := /bin/bash
.PHONY: release test


lint:
	source venv/bin/activate && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	source venv/bin/activate && flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

release:
	python3 setup.py sdist bdist_wheel
	source venv/bin/activate && twine upload dist/*

test:
	source venv/bin/activate && pytest tests.py
