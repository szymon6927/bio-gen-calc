update-deps:
	pip install pip-tools
	pip-compile --generate-hashes requirements/dev.in --output-file requirements/dev.txt
	pip-compile --generate-hashes requirements/requirements.in --output-file requirements/requirements.txt

format:
	black app --skip-string-normalization
	isort --apply

run-tests-docker:
	docker-compose -f docker-compose.local.yml exec backend pytest -v

run-tests-local:
	pytest -v

.PHONY: format update-deps
