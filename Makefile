RUN := docker compose run --rm web

make_requirements:
	$(RUN) pip-compile --generate-hashes -o requirements/prod.txt pyproject.toml
	$(RUN) pip-compile --generate-hashes -o requirements/dev.txt --extra dev pyproject.toml
