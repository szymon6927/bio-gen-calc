update-deps:
	pip install pip-tools
	pip-compile --generate-hashes requirements/dev.in --output-file requirements/dev.txt
	pip-compile --generate-hashes requirements/dev.in --output-file requirements/prod.txt

format:
	black app --skip-string-normalization
	isort --apply

.PHONY: update-deps format