SHELL := /bin/bash
.PHONY: release test

release:
	python3 -m pip install twine wheel
	python3 setup.py verify
	#python3 setup.py sdist bdist_wheel
	#twine upload dist/*

test:
	source venv/bin/activate && pytest tests.py