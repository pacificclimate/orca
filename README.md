# OPeNDAP Request Compiler Application (`orca`)

The purpose of orca is to pull apart large `OPeNDAP` requests to `THREDDS` into bite-sized chunks. These chunks are then reassembled before returning to the user.

## Installation
If you are installing the project for the first time use:
```
make
```
This will install the dependencies, run the tests and install the `pre-commit` hook for formatting. Once that is all installed you are ready to code!

`poetry` is our tool of choice for handling packages and virtual environments. Here are some commands you may want to use:
```
poetry add [package]    # install a package into the environment
poetry remove [package]  # uninstall a package from the environment
poetry run [command]        # run a command in the virtual environment
poetry lock                 # lock the current environment by updating `poetry.lock`
```
Other commands can be found in the [docs](https://pipenv.pypa.io/en/latest/).

## Run App
### Local
There are multiple ways to run `orca` on your local machine. The sections below detail the commands you'll need start up the instance that works for you.

Once an instance is running, you can request data from `orca` using a url in the following format:
```
# Generic example
http://127.0.0.1:5000/data/?filepath=[filepath]&targets=[variable][time_start:time_end][lat_start:lat_end][lon_start:lon_end]

# Example
http://127.0.0.1:5000/data/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc&targets=tasmin[0:150][0:91][0:206]
```

You can also request multiple variables, including dimension variables (e.g. time, lat, lon), but the ranges for the dimension variables and the data variables must be the same. In the example request below, the time variable is omitted, but if it were included, it would have to be specified using `time[0:150]` due to the `tasmin[0:150]` portion.
```
# Example
http://127.0.0.1:5000/data/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc&targets=lat[0:91],lon[0:206],tasmin[0:150][0:91][0:206]
```

You can also request variables without including the start and end indices, in which case the full range for each dimension is obtained. These requests can be created by having a variable with no brackets, or a variable with the bounds given by `[]` or `[:]`.
```
# Example
http://127.0.0.1:5000/data/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc&targets=time,lat[],lon[:],tasmin[0:55114][][:]
```

Finally, you can request entire data files or metadata attributes associated with the particular file.
```
# Example 1 (entire netCDF file)
http://127.0.0.1:5000/data/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc

# Example 2 (dds request)
http://127.0.0.1:5000/data/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc.dds&targets=time

# Example 3 (das request)
http://127.0.0.1:5000/data/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc.das

# Example 4 (ascii request)
http://127.0.0.1:5000/data/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc.ascii&targets=lon,lat
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
https://services.pacificclimate.org/dev/orca/?filepath=[filepath]&targets=[variable][time_start:time_end][lat_start:lat_end][lon_start:lon_end]

# Example
https://services.pacificclimate.org/dev/orca/?filepath=/storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc&targets=tasmin[0:150][0:91][0:206]
```

## Script
There is a `process.py` script in the `scripts/` subdirectory for users who would like to run ORCA through the command line. It is run with the following syntax:
```
# Example
python scripts/process.py -p /storage/data/climate/downscale/BCCAQ2/bccaqv2_with_metadata/tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc -t tasmin[0:150][0:91][0:206] -f tasmin_day_BCCAQv2+ANUSPLIN300_inmcm4_historical+rcp85_r1i1p1_19500101-21001231.nc
```