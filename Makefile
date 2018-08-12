.DEFAULT_GOAL := help

help:             ## Show available options with this Makefile
	@grep -F -h "##" $(MAKEFILE_LIST) | grep -v grep | awk 'BEGIN { FS = ":.*?##" }; { printf "%-18s  %s\n", $$1,$$2 }'

.PHONY : test
test:             ## Run all the tests
	python setup.py test

.PHONY : upload_test_pypi
upload_test_pypi: ## Build and upload distribution to testpypi server
	python setup.py sdist bdist_wheel --dist-dir dist && \
	twine upload --skip-existing --repository testpypi dist/*

.PHONY : upload_pypi
upload_pypi: ## Build and upload distribution to pypi server
	python setup.py sdist bdist_wheel --dist-dir dist && \
	twine upload --skip-existing --repository pypi dist/*

.PHONY : lint
lint: ## Run flake8 linter
	flake8 pyswitcheo tests
