# OPeNDAP Request Compiler Application (`orca`)

The purpose of orca is to pull apart large `OPeNDAP` requests to `THREDDS` into bite-sized chunks. These chunks are then reassembled before returning to the user.

## Installation
We use `make` to handle the installation process. Copy and paste this section into your terminal:
```
make
source /tmp/orca-venv/bin/activate
```

## Run App
### Local
There are multiple ways to run `orca` on your local machine. The sections below detail the commands you'll need start up the instance that works for you.

Once an instance is running, you can request data from `orca` using a url in the following format:
```
# Generic example
http://127.0.0.1:5000/data/[filepath]:[variable][time_start:time_end][lat_start:lat_end][lon_start:lon_end]

# Example
http://127.0.0.1:5000/data//storage/data/climate/downscale/CMIP5/BCSD/pr+tasmax+tasmin_day_BCSD+ANUSPLIN300+GFDL-ESM2G_historical+rcp26_r1i1p1_19500101-21001231.nc:tasmax[0:150][0:91][0:206]
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
http://docker-dev03.pcic.uvic.ca:30333/data//storage/data/climate/downscale/CMIP5/BCSD/pr+tasmax+tasmin_day_BCSD+ANUSPLIN300+GFDL-ESM2G_historical+rcp26_r1i1p1_19500101-21001231.nc:tasmax[0:150][0:91][0:206]
```
