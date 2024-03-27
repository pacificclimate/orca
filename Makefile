all: install test pre-commit-hook

install:
	curl -sSL https://install.python-poetry.org | python3 -
	poetry install
	poetry run pip install -e .

pre-commit-hook: install
	poetry run pre-commit install

test: install
	poetry run pytest -v

performance: install
	poetry run -m cProfile -o program.prof scripts/process.py -p /storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmax_day_BCCAQv2+ANUSPLIN300_CSIRO-Mk3-6-0_historical+rcp85_r1i1p1_19500101-21001231.nc -t tasmax[0:1:15000][0:1:91][0:1:206] -l DEBUG
	poetry run -m snakeviz program.prof

prod-app: install
	poetry run gunicorn --bind=0.0.0.0:5000 'orca:create_app()'

dev-app: install
	poetry run gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.DevConfig")'

test-app: install
	poetry run gunicorn --bind=0.0.0.0:5000 'orca:create_app("config.TestConfig")'

clean-tmp:
	docker exec -it orca find /tmp -name orca-output* -type f -mtime +1
