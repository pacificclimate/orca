# OPeNDAP Request Compiler Application (`orca`)

The purpose of orca is to pull apart large `OPeNDAP` requests to `THREDDS` into bite-sized chunks. These chunks are then reassembled before returning to the user.

## Installation
If you are installing the project for the first time use:
```
make
```
This will install the dependencies, run the tests and install the `pre-commit` hook for formatting. Once that is all installed you are ready to code!

`pipenv` is our tool of choice for handling packages and virtual environments. Here are some commands you may want to use:
```
pipenv install [package]    # install a package into the environment
pipenv uninstall [package]  # uninstall a package from the environment
pipenv run [command]        # run a command in the virtual environment
pipenv lock                 # lock the current environment by updating `Pipfile.lock`
```
Other commands can be found in the [docs](https://pipenv.pypa.io/en/latest/).

## Run App
### Local
There are multiple ways to run `orca` on your local machine. The sections below detail the commands you'll need start up the instance that works for you.

Once an instance is running, you can request data from `orca` using a url in the following format:
```
# Generic example
http://127.0.0.1:5000/data/[filepath]:[variable][time_start:time_end][lat_start:lat_end][lon_start:lon_end]

# Example
http://127.0.0.1:5000/data//storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc:tasmin[0:150][0:91][0:206]
```

#### `Gunicorn`
`Gunicorn` is the tool we use to deploy a robust instance of `orca` on Docker. There are 3 different options that can be started using the `Makefile`:
```
make prod-app # for production
make dev-app  # for development
make test-app # for testing
```

#### `Flask`
If you wish to run a simpler instance locally you can spin up a basic `Flask` app. Before starting the app, you'll need to point `Flask` to the app using an environment variable:
```
export FLASK_APP=wsgi.py
```

Once that has been set, use the command below to start the app:
```
flask run
```

### Docker
To run the `orca` docker container use the following:
```
docker-compose up -d
```
To stop the container:
```
docker-compose down
```

The url will be in the same format but will have a different prefix:
```
# Generic example
http://docker-dev03.pcic.uvic.ca:30333/data/[filepath]:[variable][time_start:time_end][lat_start:lat_end][lon_start:lon_end]

# Example
http://docker-dev03.pcic.uvic.ca:30333/data//storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc:tasmin[0:150][0:91][0:206]
```
