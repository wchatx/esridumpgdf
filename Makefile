SHELL := /bin/bash
.PHONY: release test

release:
	python3 -m pip install twine
	python3 setup.py verify
	echo -e "[pypi]" >> ~/.pypirc
	echo -e "username = $PYPI_USERNAME" >> ~/.pypirc
	echo -e "password = $PYPI_PASSWORD" >> ~/.pypirc
	python3 setup.py sdist bdist_wheel
	twine upload dist/*


test:
	source venv/bin/activate && pytest tests.py