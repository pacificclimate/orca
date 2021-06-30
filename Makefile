all: install test pre-commit-hook

install:
	pip install pipenv
	pipenv install

pre-commit-hook: install
	pipenv run pre-commit install

test: install
	pipenv run pytest -v

prod-app: install
	pipenv run gunicorn --bind=0.0.0.0:5000 'orca:create_app()'

dev-app: install
	pipenv run gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.DevConfig")'

test-app: install
	pipenv run gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.TestConfig")'
