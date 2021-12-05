

version:
	poetry version ${RULE}
	git tag $$(poetry version -s)
