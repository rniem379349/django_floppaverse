.PHONY: test requirements
RUN := docker compose run --rm web

requirements:
	$(RUN) pip-compile --generate-hashes -o requirements/prod.txt pyproject.toml
	$(RUN) pip-compile --generate-hashes -o requirements/dev.txt --extra dev pyproject.toml

test:
	$(RUN) pytest

collectstatic:
	$(RUN) python manage.py collectstatic
