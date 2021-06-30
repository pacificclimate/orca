all: install test pre-commit-hook

install:
	pip install pipenv
	pipenv install --dev

pre-commit-hook: install
	pipenv run pre-commit install

test: install
	pipenv run pytest -v

performance: install
	pipenv run -m cProfile -o program.prof scripts/process.py -p /storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc -t tasmax[0:1:15000][0:1:91][0:1:206] -l DEBUG
	pipenv run -m snakeviz program.prof

prod-app: install
	pipenv run gunicorn --bind=0.0.0.0:5000 'orca:create_app()'

dev-app: install
	pipenv run gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.DevConfig")'

test-app: install
	pipenv run gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.TestConfig")'
